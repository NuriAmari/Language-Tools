//
// Created by Nuri Amari on 2020-07-04.
//

#ifndef CPP_STATE_H
#define CPP_STATE_H
#include <unordered_map>
#include <unordered_set>

class NFAState {
public:
    bool m_accepting;
    std::unordered_map<char, std::unordered_set<NFAState*>> m_transitions;

    void addTransition(const char transitionChar, NFAState* target) {
        if (m_transitions.find(transitionChar) != m_transitions.end()) {
            m_transitions.at(transitionChar).insert(target);
        } else {
            m_transitions.insert({transitionChar, std::unordered_set<NFAState*>{target}});
        }
    }

    NFAState(bool accepting = false):m_accepting{accepting} { }
};

class DFAState {
public:
    bool m_accepting;
    std::unordered_map<char, DFAState*> m_transitions;

    void addTransition(const char transitionChar, DFAState* target) {
        if (m_transitions.find(transitionChar) != m_transitions.end()) {
            throw "Transition already set for DFA state";
        }
        m_transitions.insert({transitionChar, target});
    }

    DFAState(bool accepting = false):m_accepting{accepting} {}
};

#endif //CPP_STATE_H
