import io
from typing import List, Optional
from copy import deepcopy

from lexer.exceptions import LexicalError

from lexer.state import DFAState
from lexer.dfa import DFA
from lexer.token import Token


class LexerStreamReader:
    def __init__(self, stream: io.TextIOBase):
        self.stream = stream
        self.marks_stack: List[int] = []
        self.line_start_positions: List[int] = [0]

    def next(self) -> Optional[str]:
        next_char: str = self.stream.read(1)
        while next_char.isspace():
            if next_char == "\n":
                self.line_start_positions.append(self.stream.tell())
            next_char = self.stream.read(1)
        return next_char

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

    def curr_line(self) -> str:
        curr_pos = self.stream.tell()
        self.stream.seek(self.line_start_positions[-1])
        retval = self.stream.readline()
        self.stream.seek(curr_pos)
        return retval


def tokenize(input_stream, tokenizing_dfa: DFA):
    """
    Performs simplified maximal munch on the input stream
    """
    file_pos: int = 0
    last_accepting_file_pos: int = -1
    last_accepting_state: Optional[DFAState] = None
    curr_state: DFAState = tokenizing_dfa.start_state
    tokens: List[Token] = []
    curr_token: List[str] = []

    def resolve_transition_error():
        nonlocal last_accepting_state
        nonlocal input_stream
        nonlocal file_pos
        nonlocal tokens
        nonlocal curr_state
        nonlocal curr_token

        if last_accepting_state is not None:
            input_stream.seek(last_accepting_file_pos)
            file_pos = last_accepting_file_pos
            token_content = "".join(curr_token)
            try:
                tokens.append(
                    deepcopy(last_accepting_state.resolve_token(token_content))
                )
            except LexicalError:
                raise LexicalError(
                    f"LexicalError: Last accepting state at {last_accepting_file_pos} has no tokens"
                )
            last_accepting_state = None
            curr_state = tokenizing_dfa.start_state
            curr_token = []
        else:
            raise LexicalError(
                f'LexicalError: Unexpected character "{repr(transition_char)}" at position {file_pos}'
            )

    while True:
        transition_char = input_stream.read(1)
        if transition_char:
            file_pos += 1
            if transition_char.isspace():
                continue
        elif file_pos - last_accepting_file_pos == 1:
            # at EOF
            resolve_transition_error()
            break
        else:
            resolve_transition_error()

        if transition_char in curr_state.transitions:
            curr_state = curr_state.transitions[transition_char]
            curr_token.append(transition_char)
            if curr_state.accepting:
                last_accepting_state = curr_state
                last_accepting_file_pos = file_pos
        else:
            resolve_transition_error()

    return tokens
