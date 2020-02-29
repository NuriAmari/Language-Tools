from collections import defaultdict, deque
from copy import deepcopy

from lexer.state import DFAState
from lexer.exceptions import LexicalError


class DFA:

    def __init__(self, nfa_to_convert):

        # will map from a collection of nfa_states to a dfa_state
        dfa_states = dict()

        # find initial epsilon closure to start building from
        start_state = DFA.find_epsilon_closure({nfa_to_convert.start_state})

        self.start_state = DFAState(accepting=nfa_to_convert.start_state.accepting)
        dfa_states[frozenset(start_state)] = self.start_state

        q = deque([start_state])
        while q:
            curr_dfa_state = frozenset(q.pop())
            epsilon_closure = DFA.find_epsilon_closure(curr_dfa_state)

            for transition_char in nfa_to_convert.alphabet:
                transition_char_closure = set()

                for nfa_state in epsilon_closure:
                    for target_state in nfa_state.transitions[transition_char]:
                        transition_char_closure.add(target_state)

                transition_char_closure = DFA.find_epsilon_closure(transition_char_closure)
                transition_char_closure = frozenset(transition_char_closure)

                if len(transition_char_closure) > 0:

                    if transition_char_closure not in dfa_states:
                        q.appendleft(transition_char_closure)

                        is_accepting = False
                        tokens = set()

                        for state in transition_char_closure:
                            is_accepting = is_accepting or state.accepting
                            tokens = tokens.union(state.tokens)

                        dfa_states[transition_char_closure] = DFAState(accepting=is_accepting)
                        dfa_states[transition_char_closure].tokens = tokens

                    dfa_states[curr_dfa_state].set_transition(transition_char, dfa_states[transition_char_closure])

        self.states = dfa_states.values()

    def __repr__(self):
        state_strings = []
        for state in self.states:
            state_strings.append(str(state))

        return '\n'.join(state_strings)

    # @staticmethod
    # def find_closure(start_state, states_reached, symbol_to_process, symbol_used):
    #     accepting_found = False
    #     for epsilon_neighbour in start_state.transitions['']:
    #         if symbol_used:
    #             states_reached.add(epsilon_neighbour)
    #             accepting_found = accepting_found or epsilon_neighbour.accepting
    #         accepting_found = DFA.find_closure(epsilon_neighbour, states_reached, symbol_to_process, symbol_used) or accepting_found

    #     if not symbol_used:
    #         for neighbour in start_state.transitions[symbol_to_process]:
    #             states_reached.add(neighbour)
    #             accepting_found = accepting_found or neighbour.accepting
    #             accepting_found = DFA.find_closure(neighbour, states_reached, symbol_to_process, True) or accepting_found

    #     return accepting_found

    @staticmethod
    def find_epsilon_closure(states):
        states_reached = set(states)

        def helper(start_states, states_reached):
            for state in start_states:
                states_reached.add(state)
                for epsilon_neighbour in state.transitions['']:
                    if epsilon_neighbour not in states_reached:
                        helper({ epsilon_neighbour }, states_reached)

        helper(states, states_reached)
        return states_reached


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


def tokenize(input_stream, tokenizing_dfa):
    """
    Performs simplified maximal munch on the input stream
        <input_stream> The text stream providing the text to be tokenized
        <tokenizing_dfa> The dfa defining tokens
    """
    file_pos = 0
    last_accepting_file_pos = -1
    last_accepting_state = None
    curr_state = tokenizing_dfa.start_state
    tokens = []
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
            token_content = ''.join(curr_token)
            try:
                tokens.append(deepcopy(last_accepting_state.resolve_token(token_content)))
            except LexicalError:
                raise LexicalError(f'LexicalError: Last accepting state at {last_accepting_file_pos} has no tokens')
            last_accepting_state = None
            curr_state = tokenizing_dfa.start_state
            curr_token = []
        else:
            raise LexicalError(f'LexicalError: Unexpected character "{repr(transition_char)}" at position {file_pos}')

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
