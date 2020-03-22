import io

from typing import List, Tuple, Union
from langtools.lexer.exceptions import LexicalError


EOF = "EOF"


class LexerStreamReader:
    def __init__(self, stream: Union[io.TextIOBase, io.StringIO]):
        self.stream = stream
        self.marks_stack: List[int] = []
        self.line_start_positions: List[int] = [0]

    def next(self) -> str:
        next_char: str = self.stream.read(1)
        while next_char.isspace():
            if next_char == "\n":
                self.line_start_positions.append(self.stream.tell())
            next_char = self.stream.read(1)

        return next_char if next_char else EOF

    def mark(self) -> None:
        self.marks_stack.append(self.stream.tell())

    def backtrack(self) -> None:
        if self.marks_stack:
            self.stream.seek(self.marks_stack[-1])
            while (
                self.line_start_positions
                and self.line_start_positions[-1] > self.marks_stack[-1]
            ):
                self.line_start_positions.pop()
        else:
            raise LexicalError(reader=self)

    def mark_at_end(self) -> bool:
        if not self.marks_stack:
            return False
        curr_pos = self.stream.tell()
        self.stream.seek(self.marks_stack[-1])
        next_char = self.stream.read(1)

        result = True

        while next_char:
            if not next_char.isspace():
                result = False
                break
            next_char = self.stream.read(1)

        self.stream.seek(curr_pos)
        return result

    def get_curr_line(self) -> Tuple[int, int, str]:
        """
        Returns (curr_line_number, position_in_line, content_of_line)
        """
        curr_pos = self.stream.tell()
        line_start = self.line_start_positions[-1]
        self.stream.seek(line_start)
        retval = self.stream.readline()
        self.stream.seek(curr_pos)
        return (len(self.line_start_positions) - 1, curr_pos - line_start - 1, retval)
