from abc import ABC
from functools import reduce
from copy import deepcopy

from lexer.state import NFAState


class NFA(ABC):
    def __init__(self, start_state, end_state, alphabet, states):
        self.start_state = start_state
        self.end_state = end_state
        self.alphabet = alphabet
        self.states = states

    def visualize(self):
        state_ids = dict()
        num_states = 0

        for state in self.states:
            num_states += 1
            print(num_states)
            state_ids[id(state)] = num_states

        print("----")

        def state_tag(state):
            state_tag = ""
            if state.accepting:
                state_tag += "A"
            if state == self.start_state:
                state_tag += "S"
            if state.tag is not None:
                state_tag += state.tag
            return state_tag

        for state in self.states:
            state_id = state_ids[id(state)]
            for transition_char in state.transitions.keys():
                for neighbour in state.transitions[transition_char]:
                    neighbour_id = state_ids[id(neighbour)]
                    print(
                        f"{state_id}{state_tag(state)}-{transition_char}->{neighbour_id}{state_tag(neighbour)}"
                    )


class Atom(NFA):
    def __init__(self, char):
        start_state = NFAState()
        end_state = NFAState(accepting=True)
        super().__init__(
            start_state=start_state,
            end_state=end_state,
            alphabet=frozenset(char),
            states=[start_state, end_state],
        )
        self.transition_char = char
        self.start_state.add_transition(
            transition_char=char, target_state=self.end_state
        )


class Epsilon(NFA):
    def __init__(self):
        start_state = end_state = NFAState(accepting=True)
        super().__init__(
            start_state=start_state,
            end_state=end_state,
            alphabet=frozenset(),
            states=[start_state],
        )


class Union(NFA):
    def __init__(self, *operands, close=True):

        if len(operands) < 2:
            raise Exception("Union must be passed >= 2 operands")

        operands = [deepcopy(operand) for operand in operands]

        collective_alphabet = frozenset().union(
            *[operand.alphabet for operand in operands]
        )

        start_state = NFAState()
        end_state = NFAState(accepting=True)

        states = (
            [start_state]
            + reduce(lambda a, b: a + b, [operand.states for operand in operands])
            + [end_state]
        )

        super().__init__(
            start_state=start_state,
            end_state=end_state,
            alphabet=collective_alphabet,
            states=states,
        )

        for operand in operands:
            start_state.add_transition(
                transition_char="", target_state=operand.start_state
            )
            if close:
                operand.end_state.add_transition(
                    transition_char="", target_state=end_state
                )
                operand.end_state.accepting = False


class Concat(NFA):
    def __init__(self, *operands):

        if len(operands) < 2:
            raise Exception("Concat must be passed >= 2 operands")

        operands = [deepcopy(operand) for operand in operands]
        collective_alphabet = frozenset().union(
            *[operand.alphabet for operand in operands]
        )

        start_state = NFAState()
        end_state = NFAState(accepting=True)

        states = (
            [start_state]
            + reduce(lambda a, b: a + b, [operand.states for operand in operands])
            + [end_state]
        )

        super().__init__(
            start_state=start_state,
            end_state=end_state,
            alphabet=collective_alphabet,
            states=states,
        )

        start_state.add_transition(
            transition_char="", target_state=operands[0].start_state
        )

        for i in range(len(operands) - 1):
            bridge_state = NFAState(tag="B")
            self.states.append(bridge_state)
            operands[i].end_state.add_transition("", bridge_state)
            operands[i].end_state.accepting = False
            bridge_state.add_transition("", operands[i + 1].start_state)

        operands[-1].end_state.accepting = False
        operands[-1].end_state.add_transition(
            transition_char="", target_state=end_state
        )


class KleeneStar(NFA):
    def __init__(self, operand):

        operand = deepcopy(operand)

        start_state = end_state = NFAState(accepting=True, tag="KS")

        states = [start_state] + operand.states

        super().__init__(
            start_state=start_state,
            end_state=end_state,
            alphabet=operand.alphabet,
            states=states,
        )

        start_state.add_transition(transition_char="", target_state=operand.start_state)
        operand.end_state.add_transition(transition_char="", target_state=end_state)
        operand.end_state.accepting = False
