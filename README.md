# Language-Tools

A set of tools designed quickly create a lexer and parser for use in other projects. 

## Lexer Generation

### NFA Description

Tokens can be described using a set of reusable and composable regex like objects. Each represents an NFA and can be composed to quickly describe complex languages. The base objects are as follows:

**Atom**

Recognizes a single character of your choosing and nothing else:

```python
a = Atom('a')
b = Atom('b')
c = Atom('c')
```

**Epsilon**

Recognizes the empty string and nothing else:

```python
ep = Epsilon()
```

**Concat**

Consumes arbitrarily many other such objects and concatenates them together to form a new NFA:

```python
abc = Concat(a,b,c) # recognizes only "abc"
```

**Union**

As with concat, consumes arbitrarily many objects, and recognizes any of them once.

```python
a_or_b_or_c = Union(a,b,c) # recognizes "a", "b", or "c"
```

**KleeneStar**

Consumes a single NFA representation and recognizes it repeated 0 or more times

```python
a_star = KleeneStar(a) # recognizes "", "a", "aa", "aaa" ...
```

Using these objects, you can quickly recognize more complicated symbol such as the set of natural numbers:

```python
digits = [Atom(str(i)) for i in range(10)]
N = Concat(Union(*digits[1:]), KleeneStar(Union(*digits))
```

Once you've described the desired token, you can provide it with a Token object that will output if a matching string is seen. Token objects can be assigned a priority to resolve conflicts when multiple tokens match.

### DFA Creation

Given an arbitrary NFA object such as `N`, a DFA can be created:

```python
N_DFA = DFA(N)
```

This can then be used to tokenize text given a text stream like so:

```python
with open('numbers.txt') as f:
  tokens = tokenize(input_stream=f, tokenizing_dfa=N_DFA)
```

## Parsing

In order to describe a grammar, you can create a set of terminal and non-terminal symbols like this:

```python
A = NonTerminal('A')
a = Terminal('a')
```

In addition, `Epsilon` is also a type of Terminal that can be used. Next, define production rules as such:

```python
rules = [
  ProductionRule(A, [a, A]),
  ProductionRule(A, [Epsilon())
]
```

By providing an alphabet, production rules and start state, you can create a CFG object:

```python
cfg = CFG(alphabet=['a'], start_symbol=A, production_rules=rules)
```

You can then use the CFG to parse a list of tokens and validate their structure. Note currently, only LL1 parsable grammars are supported, but it will warn you if your grammar does not meet this requirement.

```python
cfg.LL1_parse(tokens)
```
