#include "Union.h"

Union::Union(Regex& first, Regex& second) : first{first}, second{second} {}

std::string Union::toString() const {
  return this->first.toString() + "|" + this->second.toString();
}
