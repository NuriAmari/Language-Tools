from lexer.nfa import Atom, Concat, Union, KleeneStar, Epsilon
from lexer.dfa import DFA

a = Atom('a')
b = Atom('b')
c = Atom('c')
d = Atom('d')
e = Atom('e')

ab = Union(a,b)
ab.visualize()
ab_star = KleeneStar(ab)
AB_STAR = DFA(ab_star)
ab_star.visualize()
AB_STAR.visualize()
