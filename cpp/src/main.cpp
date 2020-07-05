#include <iostream>
#include <string>
#include <vector>
#include "lexer/DFA.h"
#include "lexer/NFA.h"

int main() {
    Concat abc{std::vector<NFA>{{Atom{'a'},Atom{'b'}, Atom{'c'}}}};
    DFA ABC{abc};
    std::cout << ABC.match("abc") << std::endl;
    std::cout << ABC.match("abcd") << std::endl;
    std::cout << ABC.match("") << std::endl;
    return 0;
}
