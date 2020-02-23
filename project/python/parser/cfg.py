from abc import ABC
from collections import defaultdict

class CFG:

    def __init__(self, production_rules, alphabet, non_terminals, terminals):
        self.production_rules = production_rules
        self.alphabet = alphabet
        self.non_terminals = non_terminals
        self.terminals = terminals
        self._generate_parse_table()

    def _is_nullable(self, sequence, visited=None):
        if visited is None:
            visited = set()

        if not hasattr(sequence, '__iter__'):
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
                            rule_is_nullable = self._is_nullable(visited=visited, sequence=rule.rhs)

                            # if any rule is "nullable", the symbol is nullable
                            if rule_is_nullable is True:
                                symbol_is_nullable = True
                                break

                    symbol.nullable = symbol_is_nullable
                    if symbol_is_nullable is False:
                        result = False
                        break

        return result

    def _find_first(self, symbol, visited=None):

        if visited is None:
            visited = set()

        result = set()
        if symbol in visited:
            return result

        # note terminals should always have first already defined
        if symbol.first is not None:
            return symbol.first

        visited.add(symbol)
        for rule in self.production_rules:
            if rule.lhs is symbol:
                if isinstance(rule.rhs[0], Terminal) and rule.rhs[0].is_epsilon is False:
                    result = result.union(rule.rhs[0].first)
                elif isinstance(rule.rhs[0], Terminal) and rule.rhs[0].is_epsilon is True:
                    # intentionally do nothing
                    pass
                elif isinstance(rule.rhs[0], NonTerminal):
                    result = result.union(self._find_first(visited=visited, symbol=rule.rhs[0]))

        symbol.first = result
        return result


    def _find_follow(self, symbol, visited=None):

        if visited is None:
            visited = set()

        if symbol in visited:
            return set()

        if symbol.follow is not None:
            return symbol.follow

        visited.add(symbol)
        result = set()

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
                        result = result.union(self._find_first(rule.rhs[i+1]))
                        if self._is_nullable(rule.rhs[i+1]):
                            result = result.union(self._find_follow(rule.rhs[i+1], visited))
                    else:
                        result = result.union(self._find_follow(rule.lhs, visited))

        return result

    def _generate_parse_table(self):
        parse_table = defaultdict(set)
        for rule in self.production_rules:
            transition_chars = set()
            transition_chars = transition_chars.union(self._find_first(rule.rhs[0]))

            if self._is_nullable(rule.rhs[0]):
                transition_chars = transition_chars.union(self._find_follow(rule.rhs[0]))

            if self._is_nullable(rule.rhs):
                transition_chars = transition_chars.union(self._find_follow(rule.lhs))

            for char in transition_chars:
                parse_table[(rule.lhs, char)].add(rule)

        self.parse_table = parse_table

    def is_grammar_LL1(self):
        for cell in self.parse_table.values():
            if len(cell) > 1:
                return False
        return True

    def parse(self, tokens):
        pass

class ProductionRule:

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Symbol(ABC):

    def __init__(self, name, first, follow, nullable):
        self.name = name
        self.first = first
        self.follow = follow
        self.nullable = nullable

    def __repr__(self):
        return self.name

class NonTerminal(Symbol):

    def __init__(self, name):
        super(NonTerminal, self).__init__(name=name, first=None, follow=None, nullable=None)

class Terminal(Symbol):

    def __init__(self, name, first):
        first = { first } if first is not None else first
        super(Terminal, self).__init__(name=name, first=first, follow=set(), nullable=False)
        self.is_epsilon = False

class Epsilon(Terminal):

    def __init__(self):
        super().__init__(name='Epsilon', first=None)
        self.is_epsilon = True
        self.follow = set()
        self.nullable = True

class EOF(Terminal):
    pass

class BOF(Terminal):
    pass
