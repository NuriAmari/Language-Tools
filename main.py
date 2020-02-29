from json.json import LexerConfig, ParserConfig
from lexer.dfa import DFA

with open('numbers.json') as f:
    # tokens = tokenize(f, LexerConfig.TOKENIZER)
    # print(tokens)
    # # ParserConfig.JSON_GRAMMAR.print_parse_table()
    # try:
    #     ParserConfig.JSON_GRAMMAR.LL1_parse(tokens)
    # except:
    #     pass
    number = DFA(LexerConfig.NUMBER)
    if not number.match('111'):
        number.visualize()
        print('oops')
