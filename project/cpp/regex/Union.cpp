#include "Union.h"

Union::Union(std::unique_ptr<Regex>&& first, std::unique_ptr<Regex>&& second) : first{std::move(first)}, second{std::move(second)} {}

std::string Union::toString() const {
  return this->first->toString() + "|" + this->second->toString();
}
