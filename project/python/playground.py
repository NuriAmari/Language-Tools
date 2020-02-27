from lexer.nfa import Atom, Concat, Union, KleeneStar, Epsilon
from lexer.dfa import DFA
from json.json import LexerConfig

number = DFA(LexerConfig.NUMBER)

for state in number.states:
    if state.accepting:
        print('A')
        for token in state.tokens:
            print(token)
