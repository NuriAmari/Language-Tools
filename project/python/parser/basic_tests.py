import unittest

from parser.cfg import CFG, ProductionRule, NonTerminal, Terminal, Epsilon

ASCII = [chr(i) for i in range(128)]

class FirstFollowNullableTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.A = NonTerminal('A')
        cls.B = NonTerminal('B')
        cls.C = NonTerminal('C')
        cls.a = Terminal('a', first='a')
        cls.b = Terminal('b', first='b')
        cls.c = Terminal('c', first='c')
        cls.e = Epsilon()

        cls.rules = [
            ProductionRule(cls.A, [cls.e]),
            ProductionRule(cls.A, [cls.A, cls.a]),
            ProductionRule(cls.A, [cls.b]),
            ProductionRule(cls.B, [cls.c, cls.C]),
            ProductionRule(cls.A, [cls.B, cls.b]),
            ProductionRule(cls.C, [cls.e]),
        ]

        cls.cfg = CFG(production_rules=cls.rules,
                      alphabet=ASCII,
                      non_terminals={cls.A, cls.B, cls.C},
                      terminals={cls.a, cls.b, cls.c, cls.e})

    def test___is_nullable__HappyPath__CorrectResult(self):
        self.assertTrue(self.__class__.cfg._is_nullable(self.__class__.A))
        self.assertTrue(self.__class__.cfg._is_nullable(self.__class__.C))
        self.assertFalse(self.__class__.cfg._is_nullable(self.__class__.B))
        self.assertFalse(self.__class__.cfg._is_nullable(self.__class__.a))
        self.assertFalse(self.__class__.cfg._is_nullable(self.__class__.b))
        self.assertFalse(self.__class__.cfg._is_nullable(self.__class__.c))


    def test___find_first__HappyPath__CorrectSetReturned(self):
        self.assertCountEqual({'a'}, self.__class__.cfg._find_first(self.__class__.a))
        self.assertCountEqual({'b'}, self.__class__.cfg._find_first(self.__class__.b))
        self.assertCountEqual({'c'}, self.__class__.cfg._find_first(self.__class__.c))
        self.assertCountEqual({}, self.__class__.cfg._find_first(self.__class__.e))
        self.assertCountEqual({'b', 'c'}, self.__class__.cfg._find_first(self.__class__.A))
        self.assertCountEqual({'c'}, self.__class__.cfg._find_first(self.__class__.B))
        self.assertCountEqual({}, self.__class__.cfg._find_first(self.__class__.C))


    def test__find_follow__HappyPath__CorrectSetReturned(self):
        self.assertCountEqual({'a', 'b', 'c'}, self.__class__.cfg._find_follow(self.__class__.A))
        self.assertCountEqual({}, self.__class__.cfg._find_follow(self.__class__.a))
        self.assertCountEqual({}, self.__class__.cfg._find_follow(self.__class__.b))
        self.assertCountEqual({}, self.__class__.cfg._find_follow(self.__class__.c))
        self.assertCountEqual({'b'}, self.__class__.cfg._find_follow(self.__class__.B))
        self.assertCountEqual({'b'}, self.__class__.cfg._find_follow(self.__class__.C))


    def test___generate_parse_table__HappyPath__CorrectParseTable(self):
        expected_parse_table = {
            (self.__class__.A, 'a'): {self.__class__.cfg.production_rules[1], self.__class__.cfg.production_rules[0]},
            (self.__class__.A, 'b'): {self.__class__.cfg.production_rules[0], self.__class__.cfg.production_rules[1], self.__class__.cfg.production_rules[2]},
            (self.__class__.A, 'c'): {self.__class__.cfg.production_rules[0], self.__class__.cfg.production_rules[1], self.__class__.cfg.production_rules[4]},
            (self.__class__.B, 'a'): {},
            (self.__class__.B, 'b'): {},
            (self.__class__.B, 'c'): {self.__class__.cfg.production_rules[3]},
            (self.__class__.C, 'a'): {},
            (self.__class__.C, 'b'): {self.__class__.cfg.production_rules[5]},
            (self.__class__.C, 'c'): {},
        }
        for key in expected_parse_table.keys():
            self.assertCountEqual(expected_parse_table[key], self.__class__.cfg.parse_table[key])

    def test__is_grammar_LL1__HappyPath__CorrectResponse(self):
        self.assertFalse(self.__class__.cfg.is_grammar_LL1())

class LL1ParseTests(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
