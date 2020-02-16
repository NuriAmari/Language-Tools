from json.json import TOKENIZER
from lexer.dfa import tokenize

with open('test.json') as f:
    tokens = tokenize(f, TOKENIZER)
    print(tokens)
