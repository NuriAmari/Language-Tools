from collections import defaultdict
from abc import ABC, abstractmethod
from typing import Optional, Set, Dict

from langtools.lexer.exceptions import TokenResolutionError
from langtools.lexer.token import Token


class NFAState:
    def __init__(
        self, accepting: bool = False, tokens: Optional[Set[Token]] = None, tag=None
    ):
        self.transitions: Dict[str, Set[NFAState]] = defaultdict(set)
        self.accepting: bool = accepting
        self.tokens: Set[Token] = accepting and tokens or set()
        self.tag: Optional[str] = tag

    def add_transition(self, transition_char, target_state):
        self.transitions[transition_char].add(target_state)

    def show(self):
        lines = [f"{id(self)} (A: {self.accepting}):"]
        for char, targets in self.transitions.items():
            targets_string = ",".join([str(id(target)) for target in targets])
            lines.append(f"\t{char} -> {targets_string}")

        return "\n".join(lines)


class DFAState:
    def __init__(self, accepting=False, tokens=None):
        self.transitions = dict()
        self.accepting = accepting
        self.tokens = accepting and tokens or set()

    def set_transition(self, transition_char, target_state):
        self.transitions[transition_char] = target_state

    def show(self):
        lines = [f"{id(self)} (A: {self.accepting}):"]
        for char, target in self.transitions.items():
            lines.append(f"\t{char} -> {id(target)}")

        return "\n".join(lines)

    def resolve_token(self, lexme):

        # TODO: Store tokens in priority_queue in the first place
        curr_selected_token = None
        curr_priority = float("inf")

        if len(self.tokens) == 0:
            raise TokenResolutionError(f"State representing {lexme} has no tokens")

        for token in self.tokens:
            if token.priority < curr_priority:
                curr_selected_token = token
                curr_priority = token.priority
            elif token.priority == curr_priority:
                raise TokenResolutionError(
                    f"Ambiguous Tokenization: {curr_selected_token.name} - {token.name}"
                )

        curr_selected_token.lexme = lexme
        return curr_selected_token
