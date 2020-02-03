#ifndef REGEX
#define REGEX

#include <string>

class Regex {
  std::string pattern;

public:
  virtual std::string toString() const = 0;
};

#endif
