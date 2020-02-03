# Basics of Compiler Design Notes

## Chapter 1: Introduction

### 1.1 What is a compiler?

- Humans like to use high level languages
- Computers don't understand high level languages
- Compilers bridge the gap
- Somtimes we write in assembly if we want things to go really fast
    - A good compiler will come close to hand written assembly

### 1.2 The phases of a compiler

- Writing a compiler is not easy and is therefore often divided into subtasks
- These tasks or phases are often run sequentially, but not necessarily
    - Sometimes they are run in pararellel or in different orders
- Dividing each phase into its own module has several modularity related benefits
- The typical phases are as follows (usually in this order)

**Lexical Analysis:**

- Take the high level language and divide it into valid tokens
    - A list of valid tokens is defined by the high level language
    - Only if all the tokens are valid do we move onto the next phase

**Syntax Analysis:**

- Organize the tokens in a tree structure
- Validate that the arrangement of tokens is valid
- This is often called parsing

**Type Checking:**

- Verifying that types match in the context of the program

**Intermediate Code Generation:**

- Translate into a simple machine independent intermediate language
- Variable references and such are allowed in this code

**Register Allocation:**

- All generalizations are resolved to values
    - Ex jump labels replaced with jump x lines

**Machine Code Generation:**

- The intermediate language is translated into assembly

**Assembly and Linking:**

- Assembly is translated into binary representation, linked and loaded
- I don't really remember what that means


- The first three of these phases are refered to as the front end, while the last three are the backend
- Each phase ensures the next phase can make some assumptions about the format of the input

### 1.3 Interpreters

- An interpreter is an alternative to a compiler, although the two are sometimes used together
- An interpreter completes the front-end phases (lexing, parsing and type checking)
    - Rather than completing the backend, an interpreter evaluates expressions directly from the AST
    - You of course require an existing interpreter that is itself eventually compiled
- Interpreters are often slow as they must repeteadly process parts of the syntax tree
    - However, they are easier to reason about and start executing faster
    - They are often useful while developing a new language

### 1.4 Why learn about compilers?

The reasons listed are:

1. A well rounded computer scientist should know how they work
2. Understanding a compiler helps you better use one and understand the messages it relays to you
3. Parts of writing compilers is widely applicable to other areas (front-end)
4. Domain specific languages are often written to fill a small niche. Someone has to write that compiler / interpreter

Understanding how programs really run is particularly useful for understanding error messages and helps a programmer write more effectient code. Furthermore, lexing, parsing and typechecking are applicable to many different fields. Any complex file format that must be understood by a computer requires such tools.

### 1.5 - 1.8 Book specific notes

## Chapter 2: Lexical Analysis

### 2.1 Introduction

- The lexer is separated from the parser for a number of reasons (efficiency, modularity, tradition)
- It is the lexers job to tokenize the input program
- Lexers are usually created using lexer generators
    - Typically, we specify valid tokens using regular expressions
- Lexers generated as a result are in a class or programs called finite automata

### 2.2 Regular Expressions

- We use regular expressions to describe a set of strings
- There are a small set of operations and basic regular expressions used to build the rest
- You may begin with:
    - A single letter or the empty regular expression (epsilon)
- These can be combined with:
    - Or (basically union)
    - Concatenation
    - Kleene star (0 or more repitions)

The precedence of these operators is as follows:

kleene > concatenation > or
