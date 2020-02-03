#include "Concat.h"

Concat::Concat(Regex& first, Regex& second) : first{first}, second{second} {}

std::string Concat::toString() const {
  return this->first.toString() + this->second.toString();
}
