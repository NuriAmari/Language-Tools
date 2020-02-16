from lexer.nfa import Atom, Concat, Union, KleeneStar, Epsilon
from lexer.dfa import DFA

e = DFA(Epsilon())

e.visualize()
