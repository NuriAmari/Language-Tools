import io
from typing import List, Optional, Union
from copy import deepcopy

from langtools.lexer.exceptions import LexicalError, TokenResolutionError

from langtools.lexer.state import DFAState
from langtools.lexer.dfa import DFA
from langtools.lexer.token import Token
from langtools.lexer.utils import LexerStreamReader, EOF


def tokenize_str(input_str: str, tokenizing_dfa: DFA):
    return tokenize(io.StringIO(input_str), tokenizing_dfa)


def tokenize(input_stream: Union[io.TextIOBase, io.StringIO], tokenizing_dfa: DFA):
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
        nonlocal curr_state

        if last_accepting_state is not None:
            reader.pop_mark()
            resolve_token()
            last_accepting_state = None
            curr_state = tokenizing_dfa.start_state
        else:
            raise LexicalError(reader=reader)

    def resolve_token():
        nonlocal curr_lexme
        nonlocal tokens

        if curr_lexme:
            token_content = "".join(curr_lexme)
            try:
                tokens.append(
                    deepcopy(last_accepting_state.resolve_token(token_content))
                )
            except TokenResolutionError as err:
                raise LexicalError(message="TokenResolutionError", reader=reader)

            curr_lexme = []

    while True:
        transition_char = reader.next()

        if transition_char == EOF:
            if reader.mark_at_curr_pos():
                # reached EOF and tokenized entire stream
                resolve_token()
                break
            else:
                resolve_transition_error()

        if transition_char in curr_state.transitions:
            curr_state = curr_state.transitions[transition_char]
            curr_lexme.append(transition_char)
            if curr_state.accepting:
                last_accepting_state = curr_state
                reader.mark()
        else:
            resolve_transition_error()

    return tokens
