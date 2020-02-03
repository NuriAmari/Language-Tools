from lexer.tokens.symbols import INTEGER
from lexer.nfa import *
from lexer.dfa import DFA

one = Atom('1')
two = Atom('2')
three = Atom('3')

onetwothree = DFA(Concat.batch_init([one, two, three]))
print('123', onetwothree.match('123'))
