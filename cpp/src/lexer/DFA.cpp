//
// Created by Nuri Amari on 2020-07-04.
//

#include "DFA.h"

std::unordered_set<NFAState*> DFA::findEpsilonClosure(const std::unordered_set<NFAState*>& currClosure) {
    std::unordered_set<NFAState*> retval = currClosure;
    DFA::expandToEpsilonClosure(retval);
    return retval;
}

void DFA::expandToEpsilonClosure(std::unordered_set<NFAState *>& currClosure) {
    std::unordered_set<NFAState*> statesLeftToExplore = currClosure;
    while (!statesLeftToExplore.empty()) {
        for (auto it = statesLeftToExplore.begin(); it != statesLeftToExplore.end();) {
            currClosure.insert(*it);
            if ((*it)->m_transitions.find('\0') != (*it)->m_transitions.end()) {
                for (NFAState *targetState : (*it)->m_transitions.at('\0')) {
                    if (currClosure.find(targetState) == currClosure.end()) {
                        statesLeftToExplore.insert(targetState);
                    }
                }
            }
            it = statesLeftToExplore.erase(it);
        }
    }
}

DFA::DFA(const NFA& nfaToConvert) {
    std::unordered_map<std::unordered_set<NFAState*>, DFAState*, UnorderedSetHasher<NFAState*>> nfaStatesToDfaStateMap;
    std::unordered_set<NFAState*> startClosure {nfaToConvert.m_startState};
    DFA::expandToEpsilonClosure(startClosure);

    m_startState = new DFAState(nfaToConvert.m_startState->m_accepting);
    nfaStatesToDfaStateMap.insert({startClosure, m_startState});

    std::deque<std::unordered_set<NFAState*>> stateQ {startClosure};
    while (!stateQ.empty()) {
        // we call it a DFA state, but it is really a set of NFA states corresponding to an DFA state
        std::unordered_set<NFAState*> currDfaState = stateQ.front();
        std::unordered_set<NFAState*> currDfaStateEpsilonClosure = DFA::findEpsilonClosure(currDfaState);
        stateQ.pop_front();

        for (const char transitionChar : nfaToConvert.m_alphabet) {
            std::unordered_set<NFAState*> transitionCharClosure;

            for (const NFAState* epsilonNeighbour : currDfaStateEpsilonClosure) {
                if (epsilonNeighbour->m_transitions.find(transitionChar) != epsilonNeighbour->m_transitions.end()) {
                    for (NFAState* transitionNeighour : epsilonNeighbour->m_transitions.at(transitionChar)) {
                        transitionCharClosure.insert(transitionNeighour);
                    }
                }
            }

            DFA::expandToEpsilonClosure(transitionCharClosure);

            if (!transitionCharClosure.empty()) {
                // check if we already created this DFA state
                if (nfaStatesToDfaStateMap.find(transitionCharClosure) == nfaStatesToDfaStateMap.end()) {
                    stateQ.push_back(transitionCharClosure);
                    bool newStateAccepting = false;
                    for (const NFAState* state : transitionCharClosure) {
                        if (state->m_accepting) {
                            newStateAccepting = true;
                            break;
                        }
                    }
                    nfaStatesToDfaStateMap.insert({transitionCharClosure, new DFAState(newStateAccepting)});
                }

                nfaStatesToDfaStateMap.at(currDfaState)->addTransition(transitionChar, nfaStatesToDfaStateMap.at(transitionCharClosure));
            }
        }
    }

    for (std::pair<std::unordered_set<NFAState*>,DFAState*> mapping : nfaStatesToDfaStateMap) {
        m_states.insert(mapping.second);
    }
}

DFA::DFA(DFA& other) {
    *this = other;
}

DFA::DFA(DFA&& other) {
    *this = std::move(other);
}

DFA& DFA::operator=(DFA& other) {
    // given a state in the other, returns the corresponding state in the new NFA
    std::unordered_map<DFAState*, DFAState*> stateCopyMapping;

    // copy the states!
    for (DFAState* state : other.m_states) {
        DFAState* currCopy = new DFAState{state->m_accepting};
        stateCopyMapping.insert({state, currCopy});
        m_states.insert(currCopy);
    }

    // copy the transitions!
    for (DFAState* state : other.m_states) {
        for (const std::pair<char, DFAState*>& transition : state->m_transitions) {
            DFAState* startState = stateCopyMapping.at(state);
            DFAState* endState = stateCopyMapping.at(transition.second);
            if (startState->m_transitions.find(transition.first) != startState->m_transitions.end()) {
                throw "Copying this DFA went horribly wrong";
            }
            startState->addTransition(transition.first, endState);
        }
    }
    return *this;
}
DFA& DFA::operator=(DFA&& other) {
    m_startState = other.m_startState;
    m_states = std::move(other.m_states);
    return *this;
}

DFA::~DFA() {
    for (DFAState* state : m_states) {
        delete state;
    }
}

bool DFA::match(const std::string& inputStr) {
    DFAState* currState = m_startState;
    for (const char transitionChar : inputStr) {
        if (currState->m_transitions.find(transitionChar) == currState->m_transitions.end()) {
            return false;
        }
        currState = currState->m_transitions.at(transitionChar);
    }
    return currState->m_accepting;
}
