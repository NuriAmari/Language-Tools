//
// Created by Nuri Amari on 2020-07-04.
//

#include "NFA.h"

NFA::NFA(NFAState* startState, NFAState* endState, const std::unordered_set<NFAState*>& states) {
    m_startState = startState;
    m_endState = endState;
    m_states = {startState, endState};
    m_states.insert(states.begin(), states.end());
}

NFA::NFA(NFAState* startState, NFAState* endState) {
    m_startState = startState;
    m_endState = endState;
    m_states = {startState, endState};
}

NFA::NFA(NFAState* startAndEndState) {
    m_startState = startAndEndState;
    m_endState = startAndEndState;
    m_states = {startAndEndState};
}

NFA::NFA(const NFA& other) {
    *this = other;
}

NFA::NFA(NFA&& other) {
    *this = std::move(other);
}

NFA& NFA::operator=(const NFA& other) {
    // given a state in the other, returns the corresponding state in the new NFA
    std::unordered_map<NFAState*, NFAState*> stateCopyMapping;

    // copy the states
    for (NFAState* state : other.m_states) {
        NFAState* currCopy = new NFAState{state->m_accepting};
        stateCopyMapping.insert({state, currCopy});
        m_states.insert(currCopy);
    }

    // copy the transitions
    for (NFAState* state : other.m_states) {
        for (const std::pair<char, std::unordered_set<NFAState*>>& transition : state->m_transitions) {
            NFAState* startState = stateCopyMapping.at(state);
            for (NFAState* endStateToCopy : transition.second) {
                NFAState* endState = stateCopyMapping.at(endStateToCopy);
                startState->addTransition(transition.first, endState);
            }
        }
    }

    m_startState = stateCopyMapping.at(other.m_startState);
    m_endState = stateCopyMapping.at(other.m_endState);
    m_alphabet = other.m_alphabet;
    return *this;
}

NFA& NFA::operator=(NFA&& other) {
    m_startState = other.m_startState;
    m_endState = other.m_endState;
    m_states = std::move(other.m_states);
    m_alphabet = std::move(other.m_alphabet);
    return *this;
}

NFA::~NFA() {
    for (NFAState* state : m_states) {
        delete state;
    }
}

Atom::Atom(const char charToRecognize) : NFA(new NFAState(), new NFAState(true)) {
    m_startState->addTransition(charToRecognize, m_endState);
    m_alphabet.insert(charToRecognize);
}

Union::Union(std::vector<NFA>&& operands): NFA(new NFAState(), new NFAState(true)) {
    if (operands.size() < 1) {
        throw "Union expects at least one operator";
    }
    for (NFA& operand : operands) {
        m_alphabet.insert(operand.m_alphabet.begin(), operand.m_alphabet.end());
        m_startState->addTransition('\0', operand.m_startState);
        m_states.insert(operand.m_states.begin(), operand.m_states.end());
        operand.m_states.clear();
        operand.m_endState->m_accepting = false;
        operand.m_endState->addTransition('\0', m_endState);
    }
}

Concat::Concat(std::vector<NFA>&& operands) : NFA(new NFAState(), new NFAState(true)) {
    if (operands.size() < 1) {
        throw "Concat expects at least one operator";
    }
    NFA &frontOfChain = operands.front();
    NFA &backOfChain = operands.back();

    // connect start state to start of chain
    m_startState->addTransition('\0', frontOfChain.m_startState);
    for (int i = 0; i < operands.size() - 1; i++) {
        // copy the alphabet
        m_alphabet.insert(operands.at(i).m_alphabet.begin(), operands.at(i).m_alphabet.end());
        // connect pieces of the chain together
        operands.at(i).m_endState->addTransition('\0', operands.at(i + 1).m_startState);
        operands.at(i).m_endState->m_accepting = false;
        m_states.insert(operands.at(i).m_states.begin(), operands.at(i).m_states.end());
        operands.at(i).m_states.clear();
    }
    m_alphabet.insert(backOfChain.m_alphabet.begin(), backOfChain.m_alphabet.end());
    // connect end of the chain to end state
    m_states.insert(backOfChain.m_states.begin(), backOfChain.m_states.end());
    backOfChain.m_states.clear();
    backOfChain.m_endState->m_accepting = false;
    backOfChain.m_endState->addTransition('\0', m_endState);
}

Kleenestar::Kleenestar(NFA operand): NFA(new NFAState(true)) {
    m_alphabet = std::move(operand.m_alphabet);
    operand.m_endState->m_accepting = false;
    m_startState->addTransition('\0', operand.m_startState);
    operand.m_endState->addTransition('\0', m_startState);
    m_states.insert(operand.m_states.begin(), operand.m_states.end());
    operand.m_states.clear();
}

