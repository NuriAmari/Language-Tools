#include <unordered_map>

class State {
    unordered_map<char, State> transitions;
    bool accepting;
    public:
        State(bool accepting, unordered_map<char, State> transitions);            
        bool isAccepting() const;
        void setTransition(char symbol, State destination);
        void addTransition(char symbol, State destination);
};
