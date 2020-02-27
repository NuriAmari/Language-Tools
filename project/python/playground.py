from lexer.nfa import Atom, Concat, Union, KleeneStar, Epsilon
from lexer.dfa import DFA
from lexer.tokens.symbols import DIGITS, NON_ZERO_DIGITS
from json.json import LexerConfig

a = Atom('a')
b = Atom('b')
# number = KleeneStar(Union(*DIGITS))
number = Concat(Union(a,b), KleeneStar(Union(a,b)))
# number.visualize()
# number = Union(*NON_ZERO_DIGITS)

for state in number.states:
    if state.accepting:
        print('A')
        # for token in state.tokens:
        #     print(token)
