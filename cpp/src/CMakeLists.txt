project(Language-Tools)

set(LEXER_SOURCE
        lexer/DFA.cpp
        lexer/DFA.h
        lexer/NFA.h
        lexer/NFA.cpp
        lexer/State.h
        lexer/Utils.h
        )
add_library(Language-Tools STATIC ${LEXER_SOURCE})