#include "KleeneStar.h"

KleeneStar::KleeneStar(Regex& composee) : composee{composee} {}

std::string KleeneStar::toString() const {
  return "(" + this->composee.toString() + ")*";
}
