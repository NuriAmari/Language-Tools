from typing import Optional


class LexicalError(Exception):
    def __init__(self, reader, message: Optional[str] = None):
        error_line, error_col, error_line_content = reader.get_curr_line()
        error_header: str = f"LexicalError: Line {error_line}, Column {error_col}"
        error_pointer: str = " " * (error_col) + "^"
        error_char = error_line_content[error_col]
        error_message: str = message or f'Unexpected Character: "{error_char}"'

        self.error_line = error_line
        self.error_col = error_col
        self.error_char = error_char

        super().__init__(
            f"\n{error_header}\n{error_line_content}\n{error_pointer}\n{error_message}"
        )


class TokenResolutionError(Exception):
    def __init__(self, message):
        super().__init__(f"TokenResolutionError: {message}")
