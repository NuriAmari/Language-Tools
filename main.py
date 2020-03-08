from json.json import LexerConfig, ParserConfig
from lexer.dfa import DFA, tokenize
from ast.ast import ASTNode

with open("test.json") as f:
    tokens = tokenize(f, LexerConfig.TOKENIZER)
    file_tree: ASTNode = ParserConfig.JSON_GRAMMAR.LL1_parse(tokens)
    print(file_tree)
