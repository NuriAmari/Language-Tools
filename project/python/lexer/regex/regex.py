from abc import ABC, abstractmethod


class Regex(ABC):

    @abstractmethod
    def toString(self):
        pass

    def __str__(self):
        return self.toString()


class Atom(Regex):

    def __init__(self, char):
        self.char = char

    def toString(self):
        return self.char


class Epsilon(Regex):

    def toString(self):
        return 'ep'


class Union(Regex):

    def __init__(self, left_operand, right_operand):
        """ Operands should subclass from Regex """
        self.left_operand = left_operand
        self.right_operand = right_operand

    def toString(self):
        return self.left_operand.toString() + '|' + self.right_operand.toString()


class Concat(Regex):
    def __init__(self, left_operand, right_operand):
        """ Operands should subclass from Regex """
        self.left_operand = left_operand
        self.right_operand = right_operand

    def toString(self):
        return self.left_operand.toString() + self.right_operand.toString()


class KleeneStar(Regex):

    def __init__(self, operand):
        """ Operand should subclass from Regex """
        self.operand = operand

    def toString(self):
        return '(' + self.operand.toString() + ')*'
