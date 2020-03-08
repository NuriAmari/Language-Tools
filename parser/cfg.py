from abc import ABC
from collections import defaultdict
from typing import List, Iterable, Union, Set, Optional, Tuple, Dict, Callable

from parser.exceptions import ParsingException
from lexer.token import Token
from ast.ast import ASTNode


class Symbol(ABC):
    def __init__(
        self,
        name: str,
        first: Union[Set[str], None],
        follow: Optional[Set[str]],
        nullable: Optional[bool],
    ):
        self.name = name
        self.first = first
        self.follow = follow
        self.nullable = nullable

    def __repr__(self) -> str:
        return self.name


class NonTerminal(Symbol):
    def __init__(self, name):
        super(NonTerminal, self).__init__(
            name=name, first=None, follow=None, nullable=None
        )


class Terminal(Symbol):
    def __init__(self, name: str, first: Optional[Set[str]] = None):
        first = first or {name}
        super(Terminal, self).__init__(
            name=name, first=first, follow=set(), nullable=False
        )
        self.is_epsilon = False


class Epsilon(Terminal):
    def __init__(self):
        super(Epsilon, self).__init__(name="Epsilon", first=None)
        self.is_epsilon = True
        self.follow = set()
        self.nullable = True


class EOF(Terminal):
    def __init__(self):
        super(EOF, self).__init__(name="EOF")


class BOF(Terminal):
    def __init__(self):
        super(BOF, self).__init__(name="BOF")


class ProductionRule:
    def __init__(self, lhs: NonTerminal, rhs: List[Symbol], name: Optional[str] = None):
        self.lhs = lhs
        self.rhs = rhs
        self.name = name

    def __repr__(self) -> str:
        return f"{self.lhs} -> {self.rhs}"


class CFG:
    def __init__(
        self,
        production_rules: List[ProductionRule],
        alphabet: Iterable[str],
        start_symbol: NonTerminal,
        match_hook=None,
        rule_hook=None,
    ):

        self.start_prime = NonTerminal(name="S-Prime")
        self.start_symbol = start_symbol
        self.production_rules = production_rules
        self.production_rules.append(
            ProductionRule(self.start_prime, [BOF(), self.start_symbol, EOF()])
        )
        self.alphabet = alphabet
        self._generate_parse_table()
        self.match_hook: Optional[Callable[[Terminal], None]] = match_hook
        self.rule_hook: Optional[Callable[[ProductionRule], None]] = rule_hook

    def _is_nullable(
        self,
        sequence: Union[Symbol, List[Symbol]],
        visited: Optional[Set[Symbol]] = None,
    ) -> bool:

        visited = visited or set()

        if not hasattr(sequence, "__iter__"):
            sequence = [sequence]

        result = True
        for symbol in sequence:
            if symbol in visited:
                continue
            else:
                visited.add(symbol)
                if symbol.nullable is False:
                    result = False
                    break
                elif isinstance(symbol, Terminal) and symbol.is_epsilon is False:
                    result = False
                    break
                elif isinstance(symbol, NonTerminal):
                    symbol_is_nullable = False
                    for rule in self.production_rules:
                        if rule.lhs is symbol:
                            rule_is_nullable = self._is_nullable(
                                visited=visited, sequence=rule.rhs
                            )

                            # if any rule is "nullable", the symbol is nullable
                            if rule_is_nullable is True:
                                symbol_is_nullable = True
                                break

                    symbol.nullable = symbol_is_nullable
                    if symbol_is_nullable is False:
                        result = False
                        break

        return result

    def _find_first(
        self, symbol: Symbol, visited: Optional[Set[Symbol]] = None
    ) -> Set[str]:

        visited = visited or set()

        result: Set[str] = set()
        if symbol in visited:
            return result

        # note terminals should always have first already defined
        if symbol.first is not None:
            return symbol.first

        visited.add(symbol)
        for rule in self.production_rules:
            if rule.lhs is symbol:
                if (
                    isinstance(rule.rhs[0], Terminal)
                    and rule.rhs[0].is_epsilon is False
                    and rule.rhs[0].first is not None
                ):
                    result = result.union(rule.rhs[0].first)
                elif (
                    isinstance(rule.rhs[0], Terminal) and rule.rhs[0].is_epsilon is True
                ):
                    # intentionally do nothing
                    pass
                elif isinstance(rule.rhs[0], NonTerminal):
                    result = result.union(
                        self._find_first(visited=visited, symbol=rule.rhs[0])
                    )

        symbol.first = result
        return result

    def _find_follow(
        self, symbol: Symbol, visited: Optional[Set[Symbol]] = None
    ) -> Set[str]:

        visited = visited or set()

        if symbol in visited:
            return set()

        if symbol.follow is not None:
            return symbol.follow

        visited.add(symbol)
        result: Set[str] = set()

        symbol_has_left_recursive_rule = False
        for rule in self.production_rules:
            if rule.lhs is symbol and rule.rhs[0] is symbol:
                symbol_has_left_recursive_rule = True
                break

        for rule in self.production_rules:
            if symbol_has_left_recursive_rule and rule.lhs is symbol:
                result = result.union(self._find_first(rule.rhs[0]))
                if self._is_nullable(rule.rhs[0]):
                    result = result.union(self._find_follow(rule.rhs[0], visited))

            for i in range(len(rule.rhs)):
                if rule.rhs[i] is symbol:
                    if i < len(rule.rhs) - 1:
                        result = result.union(self._find_first(rule.rhs[i + 1]))
                        if self._is_nullable(rule.rhs[i + 1]):
                            result = result.union(
                                self._find_follow(rule.rhs[i + 1], visited)
                            )
                    else:
                        result = result.union(self._find_follow(rule.lhs, visited))

        return result

    def _generate_parse_table(self) -> None:
        parse_table: Dict[Tuple[NonTerminal, str], Set[ProductionRule]] = defaultdict(
            set
        )
        for rule in self.production_rules:
            transition_chars: Set[str] = set()
            transition_chars = transition_chars.union(self._find_first(rule.rhs[0]))

            if self._is_nullable(rule.rhs[0]):
                transition_chars = transition_chars.union(
                    self._find_follow(rule.rhs[0])
                )

            if self._is_nullable(rule.rhs):
                transition_chars = transition_chars.union(self._find_follow(rule.lhs))

            for char in transition_chars:
                parse_table[(rule.lhs, char)].add(rule)

        self.parse_table = parse_table

    def is_grammar_LL1(self) -> bool:
        for cell in self.parse_table.values():
            if len(cell) > 1:
                print(cell)
                return False
        return True

    def print_parse_table(self) -> None:
        for key, value in self.parse_table.items():
            print(f"{key} : {value}")

    def LL1_parse(self, tokens: List[Token]) -> ASTNode:

        root = ASTNode(name="Container")
        ast_stack: List[Tuple[ASTNode, int]] = [(root, 1)]

        if self.is_grammar_LL1():
            stack: List[Symbol] = [self.start_prime]
            tokens = [Token(name="BOF")] + tokens + [Token(name="EOF")]
            token_iterator = iter(tokens)
            curr_token = next(token_iterator)
            tokens_exhausted = False
            while stack:
                top = stack.pop()
                while isinstance(top, Epsilon):
                    top = stack.pop()
                    ast_stack[-1] = (ast_stack[-1][0], ast_stack[-1][1] - 1)
                    while len(ast_stack) > 1 and ast_stack[-1][1] == 0:
                        ast_stack.pop()
                        ast_stack[-1] = (ast_stack[-1][0], ast_stack[-1][1] - 1)
                if isinstance(top, NonTerminal):
                    correct_rule = self.parse_table[(top, curr_token.name)]
                    if len(correct_rule) < 1:
                        raise ParsingException(
                            f"ParsingException: No matching rule starting at {top}, reading {curr_token.name} found"
                        )
                    for rule in correct_rule:
                        # this will only run once
                        rule_node = ASTNode(name=rule.lhs.name)
                        ast_stack[-1][0].children.append(rule_node)
                        ast_stack.append((rule_node, len(rule.rhs)))
                        stack += list(reversed(rule.rhs))
                elif isinstance(top, Terminal):
                    if top.name == curr_token.name:
                        ast_stack[-1][0].children.append(
                            ASTNode(name=curr_token.name, lexme=curr_token.content)
                        )
                        ast_stack[-1] = (ast_stack[-1][0], ast_stack[-1][1] - 1)
                        while len(ast_stack) > 1 and ast_stack[-1][1] == 0:
                            ast_stack.pop()
                            ast_stack[-1] = (ast_stack[-1][0], ast_stack[-1][1] - 1)
                        try:
                            curr_token = next(token_iterator)
                        except StopIteration:
                            tokens_exhausted = True
                            break
                    else:
                        # TODO: Improve this error message
                        raise ParsingException(
                            f"Failed to match token: {curr_token}, top: {top}"
                        )

            if tokens_exhausted is False:
                raise ParsingException(
                    f"ParsingException: Unexpected token: {curr_token}"
                )
            elif len(stack) > 0:
                raise ParsingException(f"ParsingException: Expected more tokens")
            return root.children[0]
        else:
            raise ParsingException("Grammar must be LL1 in order to LL1 parse")
