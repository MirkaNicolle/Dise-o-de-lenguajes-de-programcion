from Thompson import regex_to_nfa, State, NFA
from Subconjuntos import visualize_automaton, nfa_to_dfa
import graphviz

def remove_unreachable_states(dfa):
    reachable = set()
    stack = [dfa.start_state]
    while stack:
        state = stack.pop()
        if state not in reachable:
            reachable.add(state)
            for symbol in state.transitions:
                stack.extend(state.transitions[symbol])

    dfa.states = [state for state in dfa.states if state in reachable]

def minimize_dfa(dfa):
    remove_unreachable_states(dfa)

    # Inicializar los conjuntos de estados: aceptación y no aceptación
    P = {frozenset([s for s in dfa.states if s.accept]), frozenset([s for s in dfa.states if not s.accept])}
    W = set(P)  # Conjuntos de trabajo, inicialmente igual a P

    while W:
        A = W.pop()
        for symbol in set(sym for state in A for sym in state.transitions):
            X = set(s for s in A if symbol in s.transitions and set(s.transitions[symbol]) & A)
            for Y in P.copy():
                intersect = X & Y
                difference = Y - X
                if intersect and difference:
                    P.remove(Y)
                    P.add(frozenset(intersect))
                    P.add(frozenset(difference))
                    if Y in W:
                        W.remove(Y)
                        W.add(frozenset(intersect))
                        W.add(frozenset(difference))
                    else:
                        W.add(frozenset(intersect) if len(intersect) <= len(difference) else frozenset(difference))

    # Crear nuevos estados para el DFA minimizado
    new_states = {frozenset(group): State(any(s.accept for s in group)) for group in P}
    start_state = next(new_states[frozenset(group)] for group in P if dfa.start_state in group)

    # Reconstruir las transiciones asegurándose de no duplicar
    for group, new_state in new_states.items():
        for symbol in set(sym for state in group for sym in state.transitions):
            # Calcula el conjunto destino para el símbolo actual
            target_set = set()
            for state in group:
                if symbol in state.transitions:
                    for target in state.transitions[symbol]:
                        target_group = next(g for g in P if target in g)
                        target_set.add(new_states[frozenset(target_group)])

            # Agrega una única transición a cada estado destino
            for target in target_set:
                new_state.add_transition(symbol, target)

    return NFA(start_state)

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
        dfa = nfa_to_dfa(nfa)  # Asegúrate de que esta función retorna un objeto NFA que representa el DFA
        minimized_dfa = minimize_dfa(dfa)
        visualize_automaton(minimized_dfa, 'Minimized DFA')
    else:
        print("Error al generar el NFA.")

if __name__ == '__main__':
    main()