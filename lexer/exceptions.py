class LexicalError(Exception):

    def __init__(self, message):
        super().__init__(f'LexicalError: {message}')
