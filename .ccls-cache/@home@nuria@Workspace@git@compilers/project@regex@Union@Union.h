#include "../Regex.h"
#include <string>

class Union : public Regex {
  Regex& first;
  Regex& second;

public:
  Union(Regex& first, Regex& second);
  std::string toString() const override;
};
