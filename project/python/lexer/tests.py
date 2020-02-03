import unittest
from unittest import TestCase

from lexer.nfa import Atom, Concat, Epsilon, KleeneStar, Union
from lexer.dfa import DFA


class AtomTests(TestCase):

    def setUp(self):
        self.a = DFA(Atom('a'))
        self.b = DFA(Atom('b'))
        self.eight = DFA(Atom('8'))
        self.comma = DFA(Atom(','))

    def test__match__HappyPath__SuccessfulMatch(self):

        self.assertTrue(self.a.match('a'))
        self.assertTrue(self.b.match('b'))
        self.assertTrue(self.eight.match('8'))
        self.assertTrue(self.comma.match(','))

    def test__match__Mismatch__UnsuccesfulMatch(self):

        self.assertFalse(self.a.match('b'))
        self.assertFalse(self.a.match('ab'))
        self.assertFalse(self.b.match('ab'))
        self.assertFalse(self.eight.match('9'))
        self.assertFalse(self.eight.match('89'))
        self.assertFalse(self.comma.match('{'))
        self.assertFalse(self.comma.match(''))

class EpsilonTests(TestCase):
    pass


class ConcatTests(TestCase):
    pass


class UnionTests(TestCase):
    pass


class KleeneStarTests(TestCase):
    pass


class RegexIntegrationTests(TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
