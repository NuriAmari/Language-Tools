from collections import defaultdict, deque

import networkx as nx
import matplotlib.pyplot as plt

from lexer.state import DFAState


class DFA:

    def __init__(self, nfa_to_convert):

        # will map from a collection of nfa_states to a dfa_state
        dfa_states = dict()

        # find initial epsilon closure to start building from
        start_state = set()
        DFA.find_epsilon_closure(nfa_to_convert.start_state, start_state)

        self.start_state = DFAState(accepting=nfa_to_convert.start_state.accepting)
        dfa_states[frozenset(start_state)] = self.start_state

        q = deque([start_state])
        while q:
            curr_dfa_state = frozenset(q.pop())

            for transition_char in nfa_to_convert.alphabet:
                transition_char_closure = set()
                is_accepting_state = False
                for nfa_state in curr_dfa_state:
                    is_accepting_state = is_accepting_state or DFA.find_closure(nfa_state, transition_char_closure, transition_char, False)
               
                transition_char_closure = frozenset(transition_char_closure)

                if len(transition_char_closure) > 0:

                    if transition_char_closure not in dfa_states:
                        q.appendleft(transition_char_closure)
                        dfa_states[transition_char_closure] = DFAState(accepting=is_accepting_state)

                    dfa_states[curr_dfa_state].set_transition(transition_char, dfa_states[transition_char_closure])

        self.states = dfa_states.values()

    def __repr__(self):
        state_strings = []
        for state in self.states:
            state_strings.append(str(state))

        return '\n'.join(state_strings)

    @staticmethod
    def find_closure(start_state, states_reached, symbol_to_process, symbol_used):
        accepting_found = False 
        for epsilon_neighbour in start_state.transitions['']:
            if symbol_used:
                states_reached.add(epsilon_neighbour)
                accepting_found = accepting_found or epsilon_neighbour.accepting
            accepting_found = DFA.find_closure(epsilon_neighbour, states_reached, symbol_to_process, symbol_used) or accepting_found

        if not symbol_used:
            for neighbour in start_state.transitions[symbol_to_process]:
                states_reached.add(neighbour)
                accepting_found = accepting_found or neighbour.accepting
                accepting_found = DFA.find_closure(neighbour, states_reached, symbol_to_process, True) or accepting_found

        return accepting_found

    @staticmethod
    def find_epsilon_closure(start_state, states_reached):
        states_reached.add(start_state)
        for epsilon_neighbour in start_state.transitions['']:
            DFA.find_epsilon_closure(epsilon_neighbour, states_reached)

    def match(self, string_to_match):
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

        print('----')

        def state_tag(state):
            state_tag = ''
            if state.accepting:
                state_tag += 'A'
            if state == self.start_state:
                state_tag += 'S'
            return state_tag

        for state in self.states:
            num_states 
            state_id = state_ids[id(state)]
            for transition_char in state.transitions.keys():
                neighbour = state.transitions[transition_char]
                neighbour_id = state_ids[id(neighbour)]
                print(f'{state_id}{state_tag(state)}-{transition_char}->{neighbour_id}{state_tag(neighbour)}')
