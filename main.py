from json.json import LexerConfig, ParserConfig, JsonObject
from lexer.dfa import DFA, tokenize
from ast.ast import ASTNode

with open("simple.json") as f:
    tokens = tokenize(f, LexerConfig.TOKENIZER)
    file_tree: ASTNode = ParserConfig.JSON_GRAMMAR.LL1_parse(tokens)
    file_tree.flatten({"ELEMENTS": "ANOTHER_ELEMENT", "MEMBERS": "ANOTHER_MEMBER"})
    json_tree = JsonObject.ast_to_object(file_tree)
    print(json_tree)
