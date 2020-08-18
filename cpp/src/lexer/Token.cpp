//
// Created by nuria on 2020-07-06.
//

#include "Token.h"

Token::Token(std::string type, int priority) {
    m_type = type;
    m_priority = priority;
}

void Token::setLexme(std::string lexme) {
    m_lexme = lexme;
}

