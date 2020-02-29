from json.json import LexerConfig, ParserConfig
from lexer.dfa import DFA, tokenize

with open('test.json') as f:
    tokens = tokenize(f, LexerConfig.TOKENIZER)
    ParserConfig.JSON_GRAMMAR.LL1_parse(tokens)
