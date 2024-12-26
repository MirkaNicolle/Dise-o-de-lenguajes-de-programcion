'''Construccion de subconjuntos es un método para convertir un Autómata Finito No Determinista (AFN) en un Autómata Finito Determinista (AFD)
Para cada nuevo estado del AFD se determina el conjunto de estados alcanzables desde cualquier estado en el conjunto actual al consumir el símbolo
Si el conjunto resultante es nuevo, se agrega como un nuevo estado en el AFD.'''

# Subconjuntos.py
import graphviz
from Thompson import regex_to_afn, State, AFN

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

def afn_to_afd(afn):
    initial_closure = epsilon_closure([afn.start_state])
    unmarked = [initial_closure]
    afd_states = {frozenset(initial_closure): State(any(s.accept for s in initial_closure))}
    afd = AFN(afd_states[frozenset(initial_closure)])

    while unmarked:
        current = unmarked.pop()
        current_state = afd_states[frozenset(current)]
        for symbol in set(sym for state in current for sym in state.transitions if sym is not None):
            move_closure = epsilon_closure(move(current, symbol))
            frozenset_closure = frozenset(move_closure)
            if frozenset_closure not in afd_states:
                afd_states[frozenset_closure] = State(any(s.accept for s in move_closure))
                unmarked.append(move_closure)
                afd.states.append(afd_states[frozenset_closure])
            target_state = afd_states[frozenset_closure]
            current_state.add_transition(symbol, target_state)
    return afd

def escape_label(text):
    return (text.replace('\\', '\\\\')
            .replace('"', '\\"')
            .replace('\n', '\\n')
            .replace('\r', '')
            .replace('{', '\\{')
            .replace('}', '\\}'))

def visualize_automaton(automaton, token_name, all_graphs):
    dot = graphviz.Digraph(name=f"digraph_afd_{token_name}", format='plain')
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
                label = escape_label(symbol) if symbol is not None else 'ε'
                dot.edge(state_name, state_names[s], label=label)

    visualize(automaton.start_state)
    all_graphs.append(dot.source)

def process_yalex_file(input_path, output_path):
    all_graphs = []
    with open(input_path, 'r') as file:
        for line in file:
            if ':=' in line:
                token_name, regex = line.split(':=', 1)
                afn = regex_to_afn(regex.strip())
                if afn:
                    afd = afn_to_afd(afn)
                    visualize_automaton(afd, token_name.strip(), all_graphs)
                else:
                    print(f"Error al generar el AFN para el token: {token_name.strip()}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(all_graphs))

def main(input_path, output_path):
    process_yalex_file(input_path, output_path)