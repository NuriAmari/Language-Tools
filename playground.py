from lexer.nfa import Atom, Concat, Union, KleeneStar, Epsilon
from lexer.dfa import DFA

a = Atom('a')
b = Atom('b')
c = Atom('c')

inner = Union(Union(a,b,c), Concat(Union(a,b), KleeneStar(Union(a,b,c))))
test = DFA(inner)

for i in range(10):
    if not test.match('aaa'):
        print('fail')
        test.visualize()
        print('---')
        inner.visualize()
        break
    else:
        print('proper')
        test.visualize()
        print('---')
        inner.visualize()
        break
