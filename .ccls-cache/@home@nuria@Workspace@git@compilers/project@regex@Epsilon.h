#include "Regex.h"
#include <string>

class Epsilon : Regex {
public:
  Epsilon();
  std::string toString() const override;
};
