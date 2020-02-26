from json.json import LexerConfig, ParserConfig
from lexer.dfa import tokenize

with open('test.json') as f:
    tokens = tokenize(f, LexerConfig.TOKENIZER)
    print(tokens)
    # ParserConfig.JSON_GRAMMAR.print_parse_table()
    # ParserConfig.JSON_GRAMMAR.LL1_parse(tokens)
