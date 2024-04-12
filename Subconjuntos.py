from Thompson import regex_to_nfa
import graphviz

class State:
    def __init__(self, accept=False):
        self.accept = accept
        self.transitions = {}

    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]

class NFA:
    def __init__(self, start_state):
        self.start_state = start_state
        self.states = [start_state]

    def add_state(self, state):
        self.states.append(state)

def epsilon_closure(states):
    stack = list(states)
    closure = set(states)
    while stack:
        state = stack.pop()
        if None in state.transitions:
            for next_state in state.transitions[None]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return closure

def move(states, symbol):
    next_states = set()
    for state in states:
        if symbol in state.transitions:
            next_states.update(state.transitions[symbol])
    return next_states

def nfa_to_dfa(nfa):
    initial_closure = epsilon_closure([nfa.start_state])
    unmarked = [initial_closure]
    dfa_states = {frozenset(initial_closure): State(any(s.accept for s in initial_closure))}
    dfa = NFA(dfa_states[frozenset(initial_closure)])

    while unmarked:
        current = unmarked.pop()
        for symbol in set(sym for state in current for sym in state.transitions if sym is not None):
            move_closure = epsilon_closure(move(current, symbol))
            frozenset_closure = frozenset(move_closure)
            if frozenset_closure not in dfa_states:
                dfa_states[frozenset_closure] = State(any(s.accept for s in move_closure))
                unmarked.append(move_closure)
                dfa.add_state(dfa_states[frozenset_closure])
            dfa_states[frozenset(current)].add_transition(symbol, dfa_states[frozenset_closure])
    return dfa

def visualize_automaton(automaton, filename='Automaton'):
    dot = graphviz.Digraph(format='png')
    seen = set()
    state_names = {}
    
    def visualize(state):
        if state in seen:
            return
        seen.add(state)
        state_name = f'S{len(seen)}'
        state_names[state] = state_name
        if state.accept:
            dot.node(state_name, shape='doublecircle')
        else:
            dot.node(state_name)
        for symbol, states in state.transitions.items():
            for s in states:
                if s not in seen:
                    visualize(s)
                dot.edge(state_name, state_names[s], label=symbol if symbol else 'ε')
    
    visualize(automaton.start_state)
    dot.render(filename, view=True)

def main():
    with open('postfix.txt', 'r') as file:
        postfix_regex = file.read().strip()
    nfa = regex_to_nfa(postfix_regex)
    if nfa:
        dfa = nfa_to_dfa(nfa)
        visualize_automaton(dfa, 'DFA_Subset')
    else:
        print("Error al generar el NFA.")

if __name__ == '__main__':
    main()