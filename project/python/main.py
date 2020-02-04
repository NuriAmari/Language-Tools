from lexer.tokens.symbols import INTEGER
from lexer.nfa import *
from lexer.dfa import DFA

test = ['123', '0123', '1', '444', '432432523532523432423', 'abc']

for num in test:
    print(num, INTEGER.match(num))
