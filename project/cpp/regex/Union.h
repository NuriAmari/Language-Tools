#include "Regex.h"
#include <string>
#include <memory>

class Union : public Regex {
  std::unique_ptr<Regex> first;
  std::unique_ptr<Regex> second;

public:
  Union(std::unique_ptr<Regex>&& first, std::unique_ptr<Regex>&& second);
  std::string toString() const override;
};
