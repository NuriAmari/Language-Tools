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

    def setUp(self):

        self.a = Atom('a')
        self.b = Atom('b')
        self.c = Atom('c')
        self.abc = DFA(Concat.batch_init([self.a, self.b, self.c]))

    def test__match__HappyPath__SuccessfulMatch(self):

        self.assertTrue(self.abc.match('abc'))

    def test__match__Mismatch__UnsuccesfulMatch(self):
        
        self.assertFalse(self.abc.match('a'))
        self.assertFalse(self.abc.match('abcd'))
        self.assertFalse(self.abc.match('d'))
        self.assertFalse(self.abc.match(''))


class UnionTests(TestCase):

    def setUp(self):

        self.a = Atom('a')
        self.b = Atom('b')
        self.c = Atom('c')
        self.a_or_b_or_c = DFA(Union.batch_init([self.a,self.b,self.c]))

    def test__match__HappyPath__SuccessfulMatch(self):

        self.assertTrue(self.a_or_b_or_c.match('a'))
        self.assertTrue(self.a_or_b_or_c.match('b'))
        self.assertTrue(self.a_or_b_or_c.match('c'))

    def test__match__Mismatch__UnsuccesfulMatch(self):

        self.assertFalse(self.a_or_b_or_c.match('d'))
        self.assertFalse(self.a_or_b_or_c.match('ab'))
        self.assertFalse(self.a_or_b_or_c.match('bc'))
        self.assertFalse(self.a_or_b_or_c.match('abc'))
        self.assertFalse(self.a_or_b_or_c.match(''))


class KleeneStarTests(TestCase):

    def setUp(self):

        self.a = Atom('a')
        self.a_star = DFA(KleeneStar(self.a))

    def test__match__HappyPath__SuccessfulMatch(self):

        self.assertTrue(self.a_star.match(''))
        self.assertTrue(self.a_star.match('a'))
        self.assertTrue(self.a_star.match('aa'))
        self.assertTrue(self.a_star.match('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'))

    def test__match__Mismatch__UnsuccesfulMatch(self):

        self.assertFalse(self.a_star.match('b'))
        self.assertFalse(self.a_star.match('ab'))
        self.assertFalse(self.a_star.match('aaaaaaaaaaaaaab'))
        self.assertFalse(self.a_star.match('baaaaaaaaaaaaaaaaaaaaaaaa'))


class RegexIntegrationTests(TestCase):

    def setUp(self):

        self.a = Atom('a')
        self.b = Atom('b')
        self.a_or_b_star = DFA(KleeneStar(Union(self.a,self.b)))

    def test__match__HappyPath__SuccessfulMatch(self):

        self.assertTrue(self.a_or_b_star.match('abababbababababababa'))
        self.assertTrue(self.a_or_b_star.match('aaaaaaaaaaaaaaaaa'))

if __name__ == '__main__':
    unittest.main()
