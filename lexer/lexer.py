import io
from typing import List, Optional
from copy import deepcopy

from lexer.exceptions import LexicalError, TokenResolutionError

from lexer.state import DFAState
from lexer.dfa import DFA
from lexer.token import Token
from lexer.utils import LexerStreamReader, EOF


def tokenize(input_stream: io.TextIOBase, tokenizing_dfa: DFA):
    """
    Performs simplified maximal munch on the input stream
    """
    last_accepting_state: Optional[DFAState] = None
    curr_state: DFAState = tokenizing_dfa.start_state
    tokens: List[Token] = []
    curr_lexme: List[str] = []  # lexme is stored in list for fast concat
    reader = LexerStreamReader(input_stream)

    def resolve_transition_error():
        nonlocal last_accepting_state
        nonlocal reader
        nonlocal tokens
        nonlocal curr_state
        nonlocal curr_lexme

        if last_accepting_state is not None:
            reader.pop_mark()
            token_content = "".join(curr_token)
            try:
                tokens.append(
                    deepcopy(last_accepting_state.resolve_token(token_content))
                )
            except TokenResolutionError as err:
                raise LexicalError(message="TokenResolutionError", reader=reader)
            last_accepting_state = None
            curr_state = tokenizing_dfa.start_state
            curr_token = []
        else:
            raise LexicalError(reader=reader)

    while True:
        transition_char = reader.next()

        if transition_char == EOF:
            if reader.mark_at_curr_pos():
                # reached EOF and tokenized entire stream
                break
            else:
                resolve_transition_error()

        if transition_char in curr_state.transitions:
            curr_state = curr_state.transitions[transition_char]
            curr_lexme.append(transition_char)
            if curr_state.accepting:
                last_accepting_state = curr_state
        else:
            resolve_transition_error()

    return tokens
