from collections import defaultdict

class State:

    def __init__(self, accepting=False):
        self.transitions = defaultdict(set)
        self.accepting = accepting
        self.in_neighbours = set()
        self.out_neighbours = set()

    def add_transition(self, transition_char, target_state):
        self.transitions[transition_char].add(target_state)
        self.out_neighbours.add(target_state)
        target_state.in_neighbours.add(self)

class DFAState:
    def __init__(self, accepting=False):
        self.transitions = dict()
        self.accepting = accepting

    def set_transition(self, transition_char, target_state):
        self.transitions[transition_char] = target_state
