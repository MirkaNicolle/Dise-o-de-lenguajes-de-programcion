'''Construccion de subconjuntos es un método para convertir un Autómata Finito No Determinista (AFN) en un Autómata Finito Determinista (AFD)
Para cada nuevo estado del AFD se determina el conjunto de estados alcanzables desde cualquier estado en el conjunto actual al consumir el símbolo
Si el conjunto resultante es nuevo, se agrega como un nuevo estado en el AFD.'''

from Thompson import regex_to_afn, AFN, State
import graphviz

'''manejo de epsilon'''
def epsilon_closure(states):
    stack = list(states)  #inicializar una pila con los estados
    closure = set(states)  #inicializar la cerradura con los mismos estados
    while stack:  #mientras haya estados en la pila
        state = stack.pop()  #sacar un estado de la pila
        if None in state.transitions:  #si hay transiciones epsilon en el estado
            for next_state in state.transitions[None]:  #iterar sobre los estados de transicion
                if next_state not in closure:  #si el estado no esta en la cerradura
                    closure.add(next_state)  #agregarlo a la cerradura
                    stack.append(next_state)  #agregarlo en la pila para explorar sus transiciones epsilon
    return closure

def move(states, symbol):
    next_states = set()  #conjunto para los estados siguientes
    for state in states:  #para cada estado en el conjunto
        if symbol in state.transitions:  #si el simbolo esta en las transiciones del estado
            next_states.update(state.transitions[symbol])  #agregar los estados de transicion al conjunto de estados siguientes
    return next_states

def afn_to_afd(afn):
    initial_closure = epsilon_closure([afn.start_state])  #obtener la cerradura epsilon del estado inicial
    unmarked = [initial_closure]  #inicializa la lista de conjuntos de estados no marcados
    afd_states = {frozenset(initial_closure): State(any(s.accept for s in initial_closure))}  #crear los estados del AFD
    afd = AFN(afd_states[frozenset(initial_closure)])  #inicializa el AFD con el estado inicial

    while unmarked:  #mientras haya conjuntos de estados no marcados
        current = unmarked.pop()  #sacar un conjunto de estados no marcado
        current_state = afd_states[frozenset(current)]  #obtener el estado del AFD correspondiente
        for symbol in set(sym for state in current for sym in state.transitions if sym is not None):  #para cada simbolo en las transiciones de los estados del conjunto
            move_closure = epsilon_closure(move(current, symbol))  #obtener la cerradura epsilon de los estados alcanzables por el simbolo
            frozenset_closure = frozenset(move_closure)  #crear un frozenset de la cerradura para usar como clave
            if frozenset_closure not in afd_states:  #si la cerradura no esta en los estados del AFD
                afd_states[frozenset_closure] = State(any(s.accept for s in move_closure))  #crear un nuevo estado en el AFD
                unmarked.append(move_closure)  #agregar la cerradura a los estados no marcados
                afd.states.append(afd_states[frozenset_closure])  #agregar el nuevo estado a los estados del AFD
            target_state = afd_states[frozenset_closure]  #obtener el estado destino del AFD
            current_state.add_transition(symbol, target_state)  #agregar la transicion al estado actual del AFD
    return afd

def visualize_automaton(automaton, filename='Automaton'):
    dot = graphviz.Digraph(format='png')
    seen = set()  #conjunto para rastrear los estados ya vistos
    state_names = {}  #diccionario para asignar nombres a los estados

    def escape_label(text):
        return (text.replace('\\', '\\\\')  #backslash
                .replace('"', '\\"')    #comillas dobles
                .replace('\n', '\\n')   #saltos de línea
                .replace('^', '\\^'))   #caret

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
