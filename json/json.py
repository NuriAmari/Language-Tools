from lexer.basic_symbols import DIGITS, NON_ZERO_DIGITS, ALPHABET, UPPERCASE_ALPHABET, ASCII
from lexer.nfa import Atom, Concat, Epsilon, KleeneStar, Union
from lexer.dfa import DFA
from lexer.token import Token

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
        ProductionRule(JSON, [VALUE]),
        ProductionRule(VALUE, [OBJECT]),
        ProductionRule(VALUE, [ARRAY]),
        ProductionRule(VALUE, [string]),
        ProductionRule(VALUE, [number]),
        ProductionRule(VALUE, [true]),
        ProductionRule(VALUE, [false]),
        ProductionRule(VALUE, [null]),
        ProductionRule(OBJECT, [left_curly, MEMBERS, right_curly]),
        ProductionRule(MEMBERS, [EpsilonGrammarSymbol()]),
        ProductionRule(MEMBERS, [MEMBER, ANOTHER_MEMBER]),
        ProductionRule(ANOTHER_MEMBER, [comma, MEMBER, ANOTHER_MEMBER]),
        ProductionRule(ANOTHER_MEMBER, [EpsilonGrammarSymbol()]),
        ProductionRule(MEMBER, [string, colon, ELEMENT]),
        ProductionRule(ARRAY, [left_square, ELEMENTS, right_square]),
        ProductionRule(ELEMENTS, [EpsilonGrammarSymbol()]),
        ProductionRule(ELEMENTS, [ELEMENT, ANOTHER_ELEMENT]),
        ProductionRule(ELEMENT, [VALUE]),
        ProductionRule(ANOTHER_ELEMENT, [comma, ELEMENT, ANOTHER_ELEMENT]),
        ProductionRule(ANOTHER_ELEMENT, [EpsilonGrammarSymbol()]),
    ]

    JSON_GRAMMAR = CFG(production_rules=PRODUCTION_RULES, alphabet=[chr(i) for i in range(128)], start_symbol=JSON)
