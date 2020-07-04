from typing import Optional


class Token:
    def __init__(self, name, lexme: Optional[str] = None, priority=1):
        self.name = name
        self.priority = priority
        self.lexme = lexme

    def __repr__(self):
        return self.name + f": {self.lexme}" if self.lexme else ""
