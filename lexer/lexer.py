from typing import List
from copy import deepcopy

from lexer.exceptions import LexicalError

from lexer.dfa import DFA
from lexer.token import Token


def tokenize(input_stream, tokenizing_dfa: DFA):
    """
    Performs simplified maximal munch on the input stream
        <input_stream> The text stream providing the text to be tokenized
        <tokenizing_dfa> The dfa defining tokens
    """
    file_pos = 0
    last_accepting_file_pos = -1
    last_accepting_state = None
    curr_state = tokenizing_dfa.start_state
    tokens: List[Token] = []
    curr_token = []

    def resolve_transition_error():
        nonlocal last_accepting_state
        nonlocal input_stream
        nonlocal file_pos
        nonlocal tokens
        nonlocal curr_state
        nonlocal curr_token

        if last_accepting_state:
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
