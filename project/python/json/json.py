from lexer.tokens.symbols import DIGITS, NON_ZERO_DIGITS, ALPHABET, UPPERCASE_ALPHABET
from lexer.nfa import Atom, Concat, Epsilon, KleeneStar, Union
from lexer.dfa import DFA
from lexer.token import Token

#################################################################################
##                                    NFAs                                     ##
#################################################################################

# General

_period = Atom('.')
COMMA = Atom(',')
COMMA.end_state.tokens.add(Token(name='COMMA', priority=1))
COLON = Atom(':')
COLON.end_state.tokens.add(Token(name='COLON', priority=1))
LEFT_CURLY = Atom('{')
LEFT_CURLY.end_state.tokens.add(Token(name='LEFT_CURLY', priority=1))
RIGHT_CURLY = Atom('}')
RIGHT_CURLY.end_state.tokens.add(Token(name='RIGHT_CURLY', priority=1))
LEFT_SQUARE = Atom('[')
LEFT_SQUARE.end_state.tokens.add(Token(name='LEFT_SQUARE', priority=1))
RIGHT_SQUARE = Atom(']')
RIGHT_SQUARE.end_state.tokens.add(Token(name='RIGHT_SQUARE', priority=1))

# Numbers

_minus = Atom('-')
_plus = Atom('+')
_sign = Union(Epsilon(), _minus, _plus)

_unsigned_integer = Union(Union(*DIGITS), Concat(Union(*NON_ZERO_DIGITS), KleeneStar(Union(*DIGITS))))
_integer = Concat(Union(_plus, Epsilon()), _unsigned_integer)

_digits = KleeneStar(Union(*DIGITS))
_fraction = Union(Epsilon(), Concat(_period, _digits))
_exponent = Union(Epsilon(), Concat(Atom('E'), _sign, _digits), Concat(Atom('e'), _sign, _digits))

NUMBER = Concat(_integer, _fraction, _exponent)
NUMBER.end_state.tokens.add(Token(name='NUMBER', priority=1))

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
STRING = Concat(Atom('"'), KleeneStar(Union(*DIGITS, *ALPHABET, *UPPERCASE_ALPHABET)), Atom('"'))
STRING.end_state.tokens.add(Token(name='STRING', priority=1))

# Booleans

TRUE = Concat(Atom('t'), Atom('r'), Atom('u'),Atom('e'))
TRUE.end_state.tokens.add(Token(name='TRUE', priority=1))
FALSE = Concat(Atom('f'), Atom('a'), Atom('l'), Atom('s'), Atom('e'))
FALSE.end_state.tokens.add(Token(name='FALSE', priority=1))

# Miscelaneous

NULL = Concat(Atom('n'), Atom('u'), Atom('l'),Atom('l'))
NULL.end_state.tokens.add(Token(name='NULL', priority=1))

TOKENIZER = DFA(Union(NUMBER, STRING, COMMA, COLON, LEFT_CURLY, RIGHT_CURLY, LEFT_SQUARE, RIGHT_SQUARE, TRUE, FALSE, NULL, close=False))
