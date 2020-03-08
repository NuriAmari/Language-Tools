from lexer.token import Token


class StringToken(Token):
    def __init__(self):
        super().__init__(name="String", priority=1)


class NumberToken(Token):
    def __init__(self):
        super().__init__(name="Number", priority=1)


class NumberToken(Token):
    def __init__(self):
        super().__init__(name="Number", priority=1)
