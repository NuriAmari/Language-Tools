from lexer.tokens.symbols import INTEGER
from lexer.nfa import *
from lexer.dfa import DFA

print('123', INTEGER.match('12334522234'))
