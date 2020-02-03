#include "../Regex.h"
#include <string>

class Concat : public Regex {
  Regex& first;
  Regex& second;

public:
  Concat(Regex& first, Regex& second);
  std::string toString() const override;
};
