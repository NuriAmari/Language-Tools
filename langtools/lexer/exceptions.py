from typing import Optional


class LexicalError(Exception):
    def __init__(self, reader, message: Optional[str] = None):
        error_line, error_col, error_line_content = reader.get_curr_line()
        error_header: str = f"LexicalError: Line {error_line}, column {error_col}"
        error_pointer: str = " " * (error_col - 1) + "^"
        error_message: str = message or ""
        super().__init__(
            f"{error_header}\n{error_line_content}\n{error_pointer}\n{error_message}"
        )


class TokenResolutionError(Exception):
    def __init__(self, message):
        super().__init__(f"TokenResolutionError: {message}")
