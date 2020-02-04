from collections import defaultdict, deque

from lexer.nfa import NFA
from lexer.state import DFAState


class DFA:

    def __init__(self, nfa_to_convert):

        # will map from a collection of nfa_states to a dfa_state
        dfa_states = dict()

        # find initial epsilon closure to start building from
        start_state = {nfa_to_convert.start_state}
        DFA.find_closure(nfa_to_convert.start_state, start_state, '')

        # determined if an accepting state lies within the epsilon closure of the start state
        start_state_is_accepting = False
        for state in start_state:
            if state.accepting:
                start_state_is_accepting = True
                break

        self.start_state = DFAState(accepting=start_state_is_accepting)

        dfa_states[frozenset(start_state)] = self.start_state

        q = deque([start_state])
        while q:
            curr_dfa_state = frozenset(q.pop())
            cut = set()
            loops = set()
            for nfa_state in curr_dfa_state:
                for transition_char in nfa_state.transitions.keys():
                    if transition_char != '' and len(nfa_state.transitions[transition_char]) > 0:
                        for neighbour in nfa_state.transitions[transition_char]:
                            if neighbour not in curr_dfa_state:
                                cut.add(transition_char)
                                break
                        else:
                            loops.add(transition_char)

            for transition_char in cut:
                transition_char_closure = set()
                is_accepting_state = False
                for nfa_state in curr_dfa_state:
                    is_accepting_state = is_accepting_state or DFA.find_closure(nfa_state, transition_char_closure, transition_char)
               
                transition_char_closure = frozenset([state for state in transition_char_closure if state not in curr_dfa_state])
                if transition_char_closure not in dfa_states:
                    q.appendleft(transition_char_closure)
                    dfa_states[transition_char_closure] = DFAState(accepting=is_accepting_state)

                dfa_states[curr_dfa_state].set_transition(transition_char, dfa_states[transition_char_closure])

            for transition_char in loops:
                dfa_states[curr_dfa_state].set_transition(transition_char, dfa_states[curr_dfa_state])

    @staticmethod
    def find_closure(start_state, states_reached, symbol_to_process):

        accepting_found = False
        for epsilon_neighbour in start_state.transitions['']:
            states_reached.add(epsilon_neighbour)
            accepting_found = accepting_found or epsilon_neighbour.accepting
            accepting_found = accepting_found or DFA.find_closure(epsilon_neighbour, states_reached, symbol_to_process)

        if symbol_to_process != '':
            for neighbour in start_state.transitions[symbol_to_process]:
                states_reached.add(neighbour)
                accepting_found = accepting_found or neighbour.accepting
                accepting_found = accepting_found or DFA.find_closure(neighbour, states_reached, '')

        return accepting_found

    def match(self, string_to_match):
        curr_state = self.start_state
        for curr_char in string_to_match:
            if curr_char in curr_state.transitions:
                curr_state = curr_state.transitions[curr_char]
            else:
                return False

        return curr_state.accepting
