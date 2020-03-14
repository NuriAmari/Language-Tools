import io

from typing import List, Tuple
from lexer.exceptions import LexicalError


EOF = "EOF"


class LexerStreamReader:
    def __init__(self, stream: io.TextIOBase):
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

    def pop_mark(self) -> None:
        if len(self.marks_stack) > 1:
            self.marks_stack.pop()
            while self.line_start_positions[-1] > self.marks_stack[-1]:
                self.line_start_positions.pop()
            self.stream.seek(self.marks_stack[-1])
        else:
            raise LexicalError("Pop called on mark stack with < 2 items")

    def mark_at_curr_pos(self) -> bool:
        return self.stream.tell() == self.marks_stack[-1]

    def get_curr_line(self) -> Tuple[int, int, str]:
        """
        Returns (curr_line_number, position_in_line, content_of_line)
        """
        curr_pos = self.stream.tell()
        line_start = self.line_start_positions[-1]
        self.stream.seek(line_start)
        retval = self.stream.readline()
        self.stream.seek(curr_pos)
        return (len(self.line_start_positions) - 1, curr_pos - line_start, retval)
