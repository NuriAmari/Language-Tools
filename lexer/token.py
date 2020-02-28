class Token:

    def __init__(self, name, priority=1):
        self.name = name
        self.priority = priority
        self.content = None

    def __repr__(self):
        return self.name + f': {self.content}' if self.content else ''
