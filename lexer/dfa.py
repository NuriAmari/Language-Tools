from typing import Dict, FrozenSet, Set
from collections import deque

from lexer.state import DFAState, NFAState


class DFA:
    def __init__(self, nfa_to_convert):

        # will map from a collection of nfa_states to a dfa_state
        dfa_states: Dict[FrozenSet[NFAState], DFAState] = dict()

        # find initial epsilon closure to start building from
        start_state: NFAState = DFA.find_epsilon_closure({nfa_to_convert.start_state})

        self.start_state: DFAState = DFAState(
            accepting=nfa_to_convert.start_state.accepting
        )
        dfa_states[frozenset(start_state)] = self.start_state

        q = deque([start_state])
        while q:
            curr_dfa_state: FrozenSet[NFAState] = frozenset(q.pop())
            epsilon_closure: Set[NFAState] = DFA.find_epsilon_closure(curr_dfa_state)

            for transition_char in nfa_to_convert.alphabet:
                transition_char_closure: Set[NFAState] = set()

                for nfa_state in epsilon_closure:
                    for target_state in nfa_state.transitions[transition_char]:
                        transition_char_closure.add(target_state)

                transition_char_closure = DFA.find_epsilon_closure(
                    transition_char_closure
                )
                transition_char_closure = frozenset(transition_char_closure)

                if len(transition_char_closure) > 0:

                    if transition_char_closure not in dfa_states:
                        q.appendleft(transition_char_closure)

                        is_accepting = False
                        tokens = set()

                        for state in transition_char_closure:
                            is_accepting = is_accepting or state.accepting
                            tokens = tokens.union(state.tokens)

                        dfa_states[transition_char_closure] = DFAState(
                            accepting=is_accepting
                        )
                        dfa_states[transition_char_closure].tokens = tokens

                    dfa_states[curr_dfa_state].set_transition(
                        transition_char, dfa_states[transition_char_closure]
                    )

        self.states = dfa_states.values()

    def __repr__(self) -> str:
        state_strings = []
        for state in self.states:
            state_strings.append(str(state))

        return "\n".join(state_strings)

    @staticmethod
    def find_epsilon_closure(states: Set[NFAState]) -> Set[NFAState]:
        states_reached: Set[NFAState] = set(states)

        def helper(start_states: Set[NFAState], states_reached: Set[NFAState]):
            for state in start_states:
                states_reached.add(state)
                for epsilon_neighbour in state.transitions[""]:
                    if epsilon_neighbour not in states_reached:
                        helper({epsilon_neighbour}, states_reached)

        helper(states, states_reached)
        return states_reached

    def match(self, string_to_match: str) -> bool:
        curr_state = self.start_state
        for curr_char in string_to_match:
            if curr_char in curr_state.transitions:
                curr_state = curr_state.transitions[curr_char]
            else:
                return False

        return curr_state.accepting

    def visualize(self):
        state_ids = dict()
        num_states = 0

        for state in self.states:
            num_states += 1
            print(num_states)
            state_ids[id(state)] = num_states

        print("----")

        def state_tag(state: DFAState) -> str:
            state_tag = ""
            if state.accepting:
                state_tag += "A"
            if state == self.start_state:
                state_tag += "S"
            return state_tag

        for state in self.states:
            state_id = state_ids[id(state)]
            for transition_char in state.transitions.keys():
                neighbour = state.transitions[transition_char]
                neighbour_id = state_ids[id(neighbour)]
                print(
                    f"{state_id}{state_tag(state)}-{transition_char}->{neighbour_id}{state_tag(neighbour)}"
                )
