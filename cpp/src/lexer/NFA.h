//
// Created by Nuri Amari on 2020-07-04.
//

#ifndef CPP_NFA_H
#define CPP_NFA_H
#include <deque>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <utility>
#include "State.h"

class NFA {
    friend class Atom;
    friend class Union;
    friend class Concat;
    friend class Kleenestar;
    friend class DFA;

    NFAState* m_startState = nullptr;
    NFAState* m_endState = nullptr;
    std::unordered_set<NFAState*> m_states;
    std::unordered_set<char> m_alphabet;

public:
    NFA() = default;
    NFA(NFAState* startState, NFAState* endState, const std::unordered_set<NFAState*>& states);
    NFA(NFAState* startState, NFAState* endState);
    NFA(NFAState* startState);

    NFA(const NFA& other);
    NFA(NFA&& other);
    NFA& operator=(const NFA& other);
    NFA& operator=(NFA&& other);
    ~NFA();
};

class Atom : public NFA {
public:
    Atom(const char charToRecognize);
};

class Union : public NFA {
public:
    Union(std::vector<NFA>&& operands);
};

class Concat : public NFA {
public:
    Concat(std::vector<NFA>&& operands);
};

class Kleenestar : public NFA {
public:
    Kleenestar(NFA operand);
};


#endif //CPP_NFA_H