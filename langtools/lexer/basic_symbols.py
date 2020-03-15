import string

from lexer.nfa import Atom, Concat, KleeneStar, Union

from lexer.dfa import DFA

ZERO = Atom("0")
ONE = Atom("1")
TWO = Atom("2")
THREE = Atom("3")
FOUR = Atom("4")
FIVE = Atom("5")
SIX = Atom("6")
SEVEN = Atom("7")
EIGHT = Atom("8")
NINE = Atom("9")

DIGITS = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]
NON_ZERO_DIGITS = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]

ALPHABET = [Atom(letter) for letter in string.ascii_lowercase]
UPPERCASE_ALPHABET = [Atom(letter) for letter in string.ascii_uppercase]

ASCII = dict()
for i in range(128):
    ASCII[chr(i)] = Atom(chr(i))
