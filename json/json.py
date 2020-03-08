from lexer.basic_symbols import DIGITS, NON_ZERO_DIGITS, ALPHABET, UPPERCASE_ALPHABET, ASCII
from lexer.nfa import Atom, Concat, Epsilon, KleeneStar, Union
from lexer.dfa import DFA
from lexer.token import Token
from ast.ast import ASTNode

from parser.cfg import CFG, Terminal, NonTerminal, ProductionRule
from parser.cfg import Epsilon as EpsilonGrammarSymbol

class LexerConfig:

    #################################################################################
    ##                                   LEXER                                     ##
    #################################################################################

    # General

    _period = Atom('.')
    COMMA = Atom(',')
    COMMA.end_state.tokens.add(Token(name='COMMA'))
    COLON = Atom(':')
    COLON.end_state.tokens.add(Token(name='COLON'))
    LEFT_CURLY = Atom('{')
    LEFT_CURLY.end_state.tokens.add(Token(name='LEFT_CURLY'))
    RIGHT_CURLY = Atom('}')
    RIGHT_CURLY.end_state.tokens.add(Token(name='RIGHT_CURLY'))
    LEFT_SQUARE = Atom('[')
    LEFT_SQUARE.end_state.tokens.add(Token(name='LEFT_SQUARE'))
    RIGHT_SQUARE = Atom(']')
    RIGHT_SQUARE.end_state.tokens.add(Token(name='RIGHT_SQUARE'))

    # Numbers

    _minus = Atom('-')
    _plus = Atom('+')
    _sign = Union(Epsilon(), _minus, _plus)

    _unsigned_integer = Union(Union(*DIGITS), Concat(Union(*NON_ZERO_DIGITS), KleeneStar(Union(*DIGITS))))
    _integer = Concat(Union(_minus, Epsilon()), _unsigned_integer)

    _digits = KleeneStar(Union(*DIGITS))
    _fraction = Union(Epsilon(), Concat(_period, _digits))
    _exponent = Union(Epsilon(), Concat(Atom('E'), _sign, _digits), Concat(Atom('e'), _sign, _digits))

    NUMBER = Concat(_integer, _fraction, _exponent)
    NUMBER.end_state.tokens.add(Token(name='NUMBER'))

    _hex_digit = Union(Atom('A'),
                       Atom('B'),
                       Atom('C'),
                       Atom('D'),
                       Atom('E'),
                       Atom('F'),
                       Atom('a'),
                       Atom('b'),
                       Atom('c'),
                       Atom('d'),
                       Atom('e'),
                       Atom('f'),
                       Union(*NON_ZERO_DIGITS))

    # Strings
    STRING = Concat(Atom('"'), Union(Epsilon(), KleeneStar(Union(*[value for key, value in ASCII.items() if key != '"']))), Atom('"'))
    STRING.end_state.tokens.add(Token(name='STRING'))

    # Booleans

    TRUE = Concat(Atom('t'), Atom('r'), Atom('u'), Atom('e'))
    TRUE.end_state.tokens.add(Token(name='TRUE'))
    FALSE = Concat(Atom('f'), Atom('a'), Atom('l'), Atom('s'), Atom('e'))
    FALSE.end_state.tokens.add(Token(name='FALSE'))

    # Miscelaneous

    NULL = Concat(Atom('n'), Atom('u'), Atom('l'), Atom('l'))
    NULL.end_state.tokens.add(Token(name='NULL'))

    TOKENIZER = DFA(Union(NUMBER, STRING, COMMA, COLON, LEFT_CURLY, RIGHT_CURLY, LEFT_SQUARE, RIGHT_SQUARE, TRUE, FALSE, NULL, close=False))


class ParserConfig:

    #################################################################################
    ##                                   PARSER                                    ##
    #################################################################################

    # NON_TERMINALS

    JSON = NonTerminal(name='JSON')
    ELEMENT = NonTerminal(name='ELEMENT')
    ANOTHER_ELEMENT = NonTerminal(name='ANOTHER_ELEMENT')
    VALUE = NonTerminal(name='VALUE')
    OBJECT = NonTerminal(name='OBJECT')
    ARRAY = NonTerminal(name='ARRAY')
    VALUE = NonTerminal(name='VALUE')
    VALUE = NonTerminal(name='VALUE')
    VALUE = NonTerminal(name='VALUE')
    MEMBERS = NonTerminal(name='MEMBERS')
    MEMBER = NonTerminal(name='MEMBER')
    ANOTHER_MEMBER = NonTerminal(name='ANOTHER_MEMBER')
    ELEMENTS = NonTerminal(name='ELEMENTS')

    # # TERMINALS

    true = Terminal(name='TRUE')
    false = Terminal(name='FALSE')
    null = Terminal(name='NULL')
    string = Terminal(name='STRING')
    number = Terminal(name='NUMBER')
    comma = Terminal(name='COMMA')
    colon = Terminal(name='COLON')
    left_curly = Terminal(name='LEFT_CURLY')
    left_square = Terminal(name='LEFT_SQUARE')
    right_curly = Terminal(name='RIGHT_CURLY')
    right_square = Terminal(name='RIGHT_SQUARE')

    # # PRODUCTION RULES

    PRODUCTION_RULES = [
        ProductionRule(JSON, [VALUE], name='SKIP'),
        ProductionRule(VALUE, [OBJECT], name='SKIP'),
        ProductionRule(VALUE, [ARRAY], name='SKIP'),
        ProductionRule(VALUE, [string], name='SKIP'),
        ProductionRule(VALUE, [number], name='SKIP'),
        ProductionRule(VALUE, [true], name='SKIP'),
        ProductionRule(VALUE, [false], name='SKIP'),
        ProductionRule(VALUE, [null], name='SKIP'),
        ProductionRule(OBJECT, [left_curly, MEMBERS, right_curly], name='OBJECT_CREATE'),
        ProductionRule(MEMBERS, [EpsilonGrammarSymbol()], name='SKIP'),
        ProductionRule(MEMBERS, [MEMBER, ANOTHER_MEMBER], name='SKIP'),
        ProductionRule(ANOTHER_MEMBER, [comma, MEMBER, ANOTHER_MEMBER], name='SKIP'),
        ProductionRule(ANOTHER_MEMBER, [EpsilonGrammarSymbol()], name='SKIP'),
        ProductionRule(MEMBER, [string, colon, ELEMENT], name='ADD_FIELD'),
        ProductionRule(ARRAY, [left_square, ELEMENTS, right_square], name='ARRAY_CREATE'),
        ProductionRule(ELEMENTS, [EpsilonGrammarSymbol()], name='SKIP'),
        ProductionRule(ELEMENTS, [ELEMENT, ANOTHER_ELEMENT], name='SKIP'),
        ProductionRule(ELEMENT, [VALUE], name='SKIP'),
        ProductionRule(ANOTHER_ELEMENT, [comma, ELEMENT, ANOTHER_ELEMENT], name='SKIP'),
        ProductionRule(ANOTHER_ELEMENT, [EpsilonGrammarSymbol()], name='SKIP'),
    ]

    JSON_GRAMMAR = CFG(production_rules=PRODUCTION_RULES, alphabet=[chr(i) for i in range(128)], start_symbol=JSON)

class JsonObject:

    def __init__(self, ast: ASTNode):
        self.content = self.__class__.ast_to_object(ast)

    @staticmethod
    def ast_to_object(ast: ASTNode) -> object:
