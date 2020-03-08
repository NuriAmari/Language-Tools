import unittest

from json.json import LexerConfig, ParserConfig
from lexer.dfa import DFA


class NumberTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.number = DFA(LexerConfig.NUMBER)
        cls.json_grammar = ParserConfig.JSON_GRAMMAR

    def test__match__HappyPath__SuccessfulMatch(self):

        self.assertTrue(self.__class__.number.match("0"))
        self.assertTrue(self.__class__.number.match("1"))
        self.assertTrue(self.__class__.number.match("-2"))
        self.assertTrue(self.__class__.number.match("3"))
        self.assertTrue(self.__class__.number.match("5"))
        self.assertTrue(self.__class__.number.match("100"))
        self.assertTrue(self.__class__.number.match("300"))
        self.assertTrue(self.__class__.number.match("123474938274981"))
        self.assertTrue(self.__class__.number.match("5829045.95849035"))
        self.assertTrue(self.__class__.number.match("4353452.00002345243"))
        self.assertTrue(self.__class__.number.match("5e34"))
        self.assertTrue(self.__class__.number.match("5e023"))
        self.assertTrue(self.__class__.number.match("5e-34"))
        self.assertTrue(self.__class__.number.match("5e-034"))
        self.assertTrue(self.__class__.number.match("5e+034"))
        self.assertTrue(self.__class__.number.match("5.0234e34"))
        self.assertTrue(self.__class__.number.match("5.0234e-34"))

    def test__match__Mismatch__UnsuccesfulMatch(self):

        self.assertFalse(self.__class__.number.match(""))
        self.assertFalse(self.__class__.number.match("02"))
        self.assertFalse(self.__class__.number.match("012"))
        self.assertFalse(self.__class__.number.match("012e5"))
        self.assertFalse(self.__class__.number.match("a12"))
        self.assertFalse(self.__class__.number.match("1A2"))

    def test__is_grammar_LL1__HappyPath__Yes(self):

        self.assertTrue(self.__class__.json_grammar.is_grammar_LL1())
