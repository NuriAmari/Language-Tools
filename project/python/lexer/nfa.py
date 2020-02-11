from abc import ABC, abstractmethod

from lexer.state import NFAState


class NFA(ABC):

    def __init__(self, start_state, end_state, alphabet):
        self.start_state = start_state
        self.end_state = end_state
        self.alphabet = alphabet

    def recognize(self, input_string):
        pass

    def to_DFA(self):
        pass

    def replace_end_state(self, new_end_state):
        for in_neighbour in self.end_state.in_neighbours:
            for target_states in in_neighbour.transitions.values():
                if self.end_state in target_states:
                    target_states.remove(self.end_state)
                    target_states.add(new_end_state)
                else:
                    print('End states should be the only path')
        self.end_state = new_end_state


class Atom(NFA):

    def __init__(self, char):
        super().__init__(start_state=NFAState(), end_state=NFAState(accepting=True), alphabet=frozenset(char))
        self.transition_char = char
        self.start_state.add_transition( transition_char=char, target_state=self.end_state)

    def __repr__(self):
        return f'{str(self.start_state)}\n{str(self.end_state)}'


class Epsilon(NFA):

    def __init__(self):
        super().__init__(start_state=NFAState(), end_state=NFAState(accepting=True))
        self.start_state.add_transition(
            transition_char='', target_state=self.end_state)

    def __repr__(self):
        return '__e__'


class Union(NFA):

    def __init__(self, *operands):

        if len(operands) < 2:
            raise Exception('Union must be passed >= 2 operands')

        collective_alphabet = frozenset().union(*[operand.alphabet for operand in operands])
        super().__init__(start_state=NFAState(), end_state=NFAState(accepting=True), alphabet=collective_alphabet)

        self.operands = operands

        for operand in operands:
            self.start_state.add_transition(
                transition_char='', target_state=operand.start_state)
            operand.replace_end_state(self.end_state)

    def __repr__(self):
        lines = [str(self.start_state)] + [str(operand) for operand in self.operands]
        return '\n'.join(lines)

class Concat(NFA):

    def __init__(self, *operands):

        if len(operands) < 2:
            raise Exception('Concat must be passed >= 2 operands')

        collective_alphabet = frozenset().union(*[operand.alphabet for operand in operands])
        super().__init__( start_state=operands[0].start_state, end_state=operands[-1].end_state, alphabet=collective_alphabet)

        self.operands = operands

        for i in range(len(operands) - 1):
            operands[i].replace_end_state(operands[i+1].start_state)

    def __repr__(self):
        lines = [str(operand) for operand in self.operands]
        return '\n'.join(lines)

class KleeneStar(NFA):

    def __init__(self, operand):
        start_state=end_state=NFAState(accepting=True)
        super().__init__(start_state=start_state, end_state=end_state, alphabet=operand.alphabet)

        self.operand=operand

        self.start_state.add_transition(
            transition_char='', target_state=operand.start_state)

        operand.replace_end_state(self.end_state)

    def __repr__(self):
        return str(self.operand)
