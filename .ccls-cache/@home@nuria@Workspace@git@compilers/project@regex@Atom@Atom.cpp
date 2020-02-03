#include "Atom.h"

Atom::Atom(char symbol): symbol{symbol} {}

std::string Atom::toString() const { return std::string(1, this->symbol); }
