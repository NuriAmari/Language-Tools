#include "Regex.h"
#include <string>

class Atom : public Regex {
  char symbol;

public:
  Atom(char symbol);
  std::string toString() const override;
};
