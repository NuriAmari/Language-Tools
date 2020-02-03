#include "./regex/Atom.h"
#include "./regex/Concat.h"
#include "./regex/KleeneStar.h"
#include "./regex/Union.h"
#include <iostream>
#include <memory>

int main() {
  Union aOrB = Union(std::make_unique<Atom>('a'), std::make_unique<Atom>('b'));
  std::cout << aOrB.toString() << std::endl;
}
