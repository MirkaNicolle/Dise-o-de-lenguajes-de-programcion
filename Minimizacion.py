'''El algoritmo de minimización para Autómatas Finitos Deterministas (AFD), reduce el número de estados al mínimo necesario para reconocer el mismo lenguaje'''

from Thompson import regex_to_afn, State, AFN
from Subconjuntos import visualize_automaton, afn_to_afd
import graphviz

def remove_unreachable_states(afd):
    reachable = set()
    stack = [afd.start_state]
    while stack:
        state = stack.pop()
        if state not in reachable:
            reachable.add(state)
            for symbol in state.transitions:
                stack.extend(state.transitions[symbol])
    afd.states = [state for state in afd.states if state in reachable]

def minimize_afd(afd):
    remove_unreachable_states(afd)
    P = {frozenset([s for s in afd.states if s.accept]), frozenset([s for s in afd.states if not s.accept])}
    B = set(P)

    while B:
        A = B.pop()
        for symbol in set(sym for state in A for sym in state.transitions):
            C = set(s for s in A if symbol in s.transitions and set(s.transitions[symbol]) & A)
            for D in P.copy():
                intersect = C & D
                difference = D - C
                if intersect and difference:
                    P.remove(D)
                    P.add(frozenset(intersect))
                    P.add(frozenset(difference))
                    if D in B:
                        B.remove(D)
                        B.add(frozenset(intersect))
                        B.add(frozenset(difference))
                    else:
                        B.add(frozenset(intersect) if len(intersect) <= len(difference) else frozenset(difference))

    new_states = {frozenset(group): State(any(s.accept for s in group)) for group in P}
    start_state = next(new_states[frozenset(group)] for group in P if afd.start_state in group)
    for group, new_state in new_states.items():
        for symbol in set(sym for state in group for sym in state.transitions):
            target_set = set()
            for state in group:
                if symbol in state.transitions:
                    for target in state.transitions[symbol]:
                        target_group = next(g for g in P if target in g)
                        target_set.add(new_states[frozenset(target_group)])
            for target in target_set:
                new_state.add_transition(symbol, target)

    return AFN(start_state)

def visualize_automaton(automaton, token_name, all_graphs):
    dot = graphviz.Digraph(name=f"digraph_afd_{token_name}", format='plain')
    seen = set()
    state_names = {}

    def escape_label(text):
        # Escapar los caracteres especiales para Graphviz
        return (text.replace('\\', '\\\\')  # Escapa el backslash
                .replace('"', '\\"')    # Escapa las comillas dobles
                .replace('\n', '\\n')   # Escapa los saltos de línea
                .replace('^', '\\^'))   # Escapa el caret

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
                label = escape_label(symbol) if symbol is not None else 'ε'
                dot.edge(state_name, state_names[s], label=label)

    visualize(automaton.start_state)
    all_graphs.append(dot.source)  # Agregar el grafo al listado general

def process_yalex_file(input_path, output_filename):
    all_graphs = []  # Lista para acumular todos los grafos
    with open(input_path, 'r') as file:
        for line in file:
            if ':=' in line:
                token_name, regex = line.split(':=')
                regex = regex.strip()
                afn = regex_to_afn(regex)
                if afn:
                    afd = afn_to_afd(afn)
                    minimized_afd = minimize_afd(afd)
                    visualize_automaton(minimized_afd, token_name, all_graphs)
                else:
                    print(f"Error al generar el AFN para el token: {token_name}")

    # Guardar todos los grafos en un archivo
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(all_graphs))

def main(input_path, output_path):
    process_yalex_file(input_path, output_path)