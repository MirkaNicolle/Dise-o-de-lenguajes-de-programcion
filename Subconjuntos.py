'''Construccion de subconjuntos es un método para convertir un Autómata Finito No Determinista (AFN) en un Autómata Finito Determinista (AFD)
Para cada nuevo estado del AFD se determina el conjunto de estados alcanzables desde cualquier estado en el conjunto actual al consumir el símbolo
Si el conjunto resultante es nuevo, se agrega como un nuevo estado en el AFD.'''

from Thompson import regex_to_afn, AFN, State
import graphviz

'''manejo de epsilon'''
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
    print(f"Initial epsilon closure: {initial_closure}")  # Depuración
    unmarked = [initial_closure]
    afd_states = {frozenset(initial_closure): State(any(s.accept for s in initial_closure))}
    afd = AFN(afd_states[frozenset(initial_closure)])
    print(f"Initial AFD state: {afd_states}")  # Depuración

    while unmarked:
        current = unmarked.pop()
        print(f"Processing: {current}")  # Depuración
        current_state = afd_states[frozenset(current)]
        for symbol in set(sym for state in current for sym in state.transitions if sym is not None):
            move_closure = epsilon_closure(move(current, symbol))
            print(f"Move closure for symbol {symbol}: {move_closure}")  # Depuración
            frozenset_closure = frozenset(move_closure)
            if frozenset_closure not in afd_states:
                afd_states[frozenset_closure] = State(any(s.accept for s in move_closure))
                unmarked.append(move_closure)
                afd.states.append(afd_states[frozenset_closure])
            target_state = afd_states[frozenset_closure]
            current_state.add_transition(symbol, target_state)
            print(f"Transition added: {current_state} --{symbol}--> {target_state}")  # Depuración
    return afd

def visualize_automaton(automaton, filename='Automaton'):
    dot = graphviz.Digraph(format='png')
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
    output_path = f'{filename}.gv'
    dot.render(output_path, view=True)
    #print(f"Automaton visualized in: {output_path}.png")

def process_yalex_file(input_path):
    with open(input_path, 'r') as file:
        for line in file:
            if ':=' in line:
                token_name, regex = line.split(':=')
                regex = regex.strip()
                afn = regex_to_afn(regex)
                if afn:
                    afd = afn_to_afd(afn)
                    visualize_automaton(afd, f'Subconjuntos_AFD_{token_name}')
                else:
                    print(f"Error al generar el AFN para el token: {token_name}")

def main():
    process_yalex_file('output_postfix.yalex')

if __name__ == '__main__':
    main()