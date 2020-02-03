from abc import ABC, abstractmethod

from lexer.state import State


class NFA(ABC):

    def __init__(self, start_state, end_state):
        self.start_state = start_state
        self.end_state = end_state

    def __str__(self):
        return self.to_string()

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

    @abstractmethod
    def to_string(self):
        pass


class Atom(NFA):

    def __init__(self, char):
        super().__init__(start_state=State(), end_state=State(accepting=True))
        self.transition_char = char
        self.start_state.add_transition(
            transition_char=char, target_state=self.end_state)

    def to_string(self):
        return self.transition_char


class Epsilon(NFA):

    def __init__(self):
        super().__init__(start_state=State(), end_state=State(accepting=True))
        self.start_state.add_transition(
            transition_char='', target_state=self.end_state)

    def to_string(self):
        return '__e__'


class Union(NFA):

    def __init__(self, left_operand, right_operand):
        super().__init__(start_state=State(), end_state=State(accepting=True))

        self.left_operand = left_operand
        self.right_operand = right_operand

        self.start_state.add_transition( transition_char='', target_state=left_operand.start_state)
        self.start_state.add_transition( transition_char='', target_state=right_operand.start_state)

        left_operand.replace_end_state(self.end_state)
        right_operand.replace_end_state(self.end_state)

    @classmethod
    def batch_init(cls, batch, batch_cursor=0):
        if len(batch) - batch_cursor < 2:
           raise Exception('Union batch_init requires batch size >= 2') 
        if len(batch) - batch_cursor == 2:
            return cls(left_operand=batch[batch_cursor], right_operand=batch[batch_cursor+1])
        else:
            return cls(left_operand=batch[batch_cursor], right_operand=cls.batch_init(batch, batch_cursor + 1))


    def to_string(self):
        return self.left_operand.to_string() + '|' + self.right_operand.to_string()

class Concat(NFA):
    def __init__(self, left_operand, right_operand):
        super().__init__(start_state=left_operand.start_state, end_state=right_operand.end_state)
        print('b.end', id(right_operand.end_state), 'cab.end', id(self.end_state))
        self.left_operand = left_operand
        self.right_operand = right_operand

        left_operand.replace_end_state(right_operand.start_state)


    @classmethod
    def batch_init(cls, batch, batch_cursor=0):
        if len(batch) - batch_cursor < 2:
           raise Exception('Concat batch_init requires batch size >= 2') 
        if len(batch) - batch_cursor == 2:
            return cls(left_operand=batch[batch_cursor], right_operand=batch[batch_cursor+1])
        else:
            return cls(left_operand=batch[batch_cursor], right_operand=cls.batch_init(batch, batch_cursor + 1))

    def to_string(self):
        return self.left_operand.to_string() + self.right_operand.to_string()


class KleeneStar(NFA):

    def __init__(self, operand):
        start_state = end_state = State(accepting=True)
        super().__init__(start_state=start_state, end_state=end_state) 

        self.operand = operand

        self.start_state.add_transition(transition_char='', target_state=operand.start_state)

        operand.replace_end_state(self.end_state)

    def to_string(self):
        return '(' + self.operand.to_string() + ')*'
