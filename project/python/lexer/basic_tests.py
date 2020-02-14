import unittest

from lexer.nfa import *
from lexer.dfa import DFA


class AtomTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a = DFA(Atom('a'))
        cls.b = DFA(Atom('b'))
        cls.eight = DFA(Atom('8'))
        cls.comma = DFA(Atom(','))

    def test__match__HappyPath__SuccessfulMatch(self):

        self.assertTrue(self.__class__.a.match('a'))
        self.assertTrue(self.__class__.b.match('b'))
        self.assertTrue(self.__class__.eight.match('8'))
        self.assertTrue(self.__class__.comma.match(','))

    def test__match__Mismatch__UnsuccesfulMatch(self):

        self.assertFalse(self.__class__.a.match('b'))
        self.assertFalse(self.__class__.a.match('ab'))
        self.assertFalse(self.__class__.b.match('ab'))
        self.assertFalse(self.__class__.eight.match('9'))
        self.assertFalse(self.__class__.eight.match('89'))
        self.assertFalse(self.__class__.comma.match('{'))
        self.assertFalse(self.__class__.comma.match(''))


class ConcatTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a = Atom('a')
        cls.b = Atom('b')
        cls.c = Atom('c')
        cls.abc = DFA(Concat(cls.a, cls.b, cls.c))

    def test__match__HappyPath__SuccessfulMatch(self):

        self.assertTrue(self.__class__.abc.match('abc'))

    def test__match__Mismatch__UnsuccesfulMatch(self):

        self.assertFalse(self.__class__.abc.match('a'))
        self.assertFalse(self.__class__.abc.match('abcd'))
        self.assertFalse(self.__class__.abc.match('d'))
        self.assertFalse(self.__class__.abc.match(''))


class UnionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a = Atom('a')
        cls.b = Atom('b')
        cls.c = Atom('c')
        cls.a_or_b_or_c = DFA(Union(cls.a, cls.b, cls.c))

    def test__match__HappyPath__SuccessfulMatch(self):

        self.assertTrue(self.__class__.a_or_b_or_c.match('a'))
        self.assertTrue(self.__class__.a_or_b_or_c.match('b'))
        self.assertTrue(self.__class__.a_or_b_or_c.match('c'))

    def test__match__Mismatch__UnsuccesfulMatch(self):

        self.assertFalse(self.__class__.a_or_b_or_c.match('d'))
        self.assertFalse(self.__class__.a_or_b_or_c.match('ab'))
        self.assertFalse(self.__class__.a_or_b_or_c.match('bc'))
        self.assertFalse(self.__class__.a_or_b_or_c.match('abc'))
        self.assertFalse(self.__class__.a_or_b_or_c.match(''))


class KleeneStarTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.a = Atom('a')
        cls.a_star = DFA(KleeneStar(cls.a))

    def test__match__HappyPath__SuccessfulMatch(self):

        self.assertTrue(self.__class__.a_star.match(''))
        self.assertTrue(self.__class__.a_star.match('a'))
        self.assertTrue(self.__class__.a_star.match('aa'))
        self.assertTrue(self.__class__.a_star.match(
            'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'))

    def test__match__Mismatch__UnsuccesfulMatch(self):

        self.assertFalse(self.__class__.a_star.match('b'))
        self.assertFalse(self.__class__.a_star.match('ab'))
        self.assertFalse(self.__class__.a_star.match('aaaaaaaaaaaaaab'))
        self.assertFalse(self.__class__.a_star.match(
            'baaaaaaaaaaaaaaaaaaaaaaaa'))


class RegexIntegrationTests(unittest.TestCase):

    def setUp(self):

        self.a = Atom('a')
        self.b = Atom('b')
        self.a_or_b_star = DFA(KleeneStar(Union(self.a, self.b)))
        self.ab_star = DFA(KleeneStar(Concat(self.a, self.b)))

    def test__match__HappyPath__SuccessfulMatch(self):

        self.assertTrue(self.a_or_b_star.match('abababbababababababa'))
        self.assertTrue(self.a_or_b_star.match(''))
        self.assertTrue(self.a_or_b_star.match('aaaaaaaaaaaaaaaaa'))
        self.assertTrue(self.ab_star.match(''))
        self.assertTrue(self.ab_star.match('ab'))
        self.assertTrue(self.ab_star.match('ababababababababababab'))

    def test__match__Mismatch__SuccessfulMatch(self):

        self.assertFalse(self.ab_star.match('a'))
        self.assertFalse(self.ab_star.match('aba'))
        self.assertFalse(self.ab_star.match('ba'))
        self.assertFalse(self.a_or_b_star.match('abc'))

if __name__ == '__main__':
    unittest.main()
