#include "State.h"

State::State(bool accepting, unordered_map<char, State> transitions) {
    this.accepting = accepting;
    this.transitions = transitions;
}

bool State::isAccepting() const {
    return this.accepting;
}

void State::setTransition(char symbol, State destination) {
    this.transitions.at(symbol) = destination;    
}

void State::addTransition(char symbol, State destination) {
    this.transitions[symbol] = destination;
}
