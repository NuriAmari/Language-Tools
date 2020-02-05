from lexer.tokens.symbols import INTEGER
from lexer.nfa import *
from lexer.dfa import DFA

tests = ['1', '2', '123', '0123', 'abc', '50a']

for test in tests:
    print(test, INTEGER.match(test))


a = Atom('a')
b = Atom('b')
test = DFA(Union(a,b))
# print(a_or_b_or_c.match('a'), True)
# print(a_or_b_or_c.match('b'), True)
# print(a_or_b_or_c.match('c'), True)
# print(a_or_b_or_c.match('d'), False)
# print(a_or_b_or_c.match('ab'), False)
# print(a_or_b_or_c.match('bc'), False)
# print(a_or_b_or_c.match('abc'), False)
# print(a_or_b_or_c.match(''), False)

# print(a_or_b_or_c)
# print('------')
print(test)
