#include "../Regex.h"
#include <string>

class KleeneStar : public Regex {
  Regex& composee;

public:
  KleeneStar(Regex& composee);
  std::string toString() const override;
};
