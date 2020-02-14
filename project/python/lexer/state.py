from collections import defaultdict
from abc import ABC, abstractmethod

class NFAState:

    def __init__(self, accepting=False):
        self.transitions = defaultdict(set)
        self.accepting = accepting

    def add_transition(self, transition_char, target_state):
        self.transitions[transition_char].add(target_state)

    def show(self):
        lines = [f'{id(self)} (A: {self.accepting}):']
        for char, targets in self.transitions.items():
            targets_string = ','.join([str(id(target)) for target in targets])
            lines.append(f'\t{char} -> {targets_string}')

        return '\n'.join(lines)

class DFAState:
    def __init__(self, accepting=False):
        self.transitions = dict()
        self.accepting = accepting

    def set_transition(self, transition_char, target_state):
        self.transitions[transition_char] = target_state

    def show(self):
        lines = [f'{id(self)} (A: {self.accepting}):']
        for char, target in self.transitions.items():
            lines.append(f'\t{char} -> {id(target)}')

        return '\n'.join(lines)
