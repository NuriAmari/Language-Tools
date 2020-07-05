//
// Created by Nuri Amari on 2020-07-04.
//

#ifndef CPP_DFA_H
#define CPP_DFA_H
#include <unordered_set>
#include <string>
#include <iostream>
#include "NFA.h"
#include "State.h"
#include "Utils.h"

class DFA {
    DFAState* m_startState;
    std::unordered_set<DFAState*> m_states;
    static std::unordered_set<NFAState*> findEpsilonClosure(const std::unordered_set<NFAState*>& currClosure);
    static void expandToEpsilonClosure(std::unordered_set<NFAState*>& currClosure);

public:
    DFA(const NFA& nfaToConvert);
    DFA(DFA& other);
    DFA(DFA&& other);
    DFA& operator=(DFA& other);
    DFA& operator=(DFA&& other);
    ~DFA();

    bool match(const std::string& inputStr);
};


#endif //CPP_DFA_H
