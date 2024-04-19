'''Construccion de subconjuntos es un método para convertir un Autómata Finito No Determinista (AFN) en un Autómata Finito Determinista (AFD)
Para cada nuevo estado del AFD se determina el conjunto de estados alcanzables desde cualquier estado en el conjunto actual al consumir el símbolo
Si el conjunto resultante es nuevo, se agrega como un nuevo estado en el AFD.'''

import graphviz  
from Thompson import regex_to_afn, State, AFN  # 

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

def move(states, symbol):  #obtencion del conjunto de estados alcanzables desde un conjunto dado por un simbolo
    next_states = set()  #conjunto para los estados siguientes
    for state in states:  #para cada estado en el conjunto
        if symbol in state.transitions:  #si el simbolo esta en las transiciones del estado
            next_states.update(state.transitions[symbol])  #agregar los estados de transicion al conjunto de estados siguientes
    return next_states  #devolver el conjunto de estados siguientes

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
    return afd  # devolver el AFD

def escape_label(text): 
    return (text.replace('\\', '\\\\')  
            .replace('"', '\\"')       
            .replace('\n', '\\n')      
            .replace('\r', '')         
            .replace('{', '\\{')       
            .replace('}', '\\}'))      

def visualize_automaton(automaton, token_name, all_graphs):  
    dot = graphviz.Digraph(name=f"digraph_afd_{token_name}", format='plain')  #crear un grafo dirigido con el nombre especificado
    seen = set()  #conjunto para rastrear los estados ya vistos
    state_names = {}  #diccionario para asignar nombres a los estados

    def visualize(state):  
        if state in seen:  #si el estado ya fue visualizado
            return
        seen.add(state)  #marcar el estado como visto
        state_name = f'S{len(seen)}'  #asignar un nombre al estado basado en el orden de visualizacion
        state_names[state] = state_name  #guardar el nombre asignado al estado
        if state.accept:  #si el estado es de aceptacion
            dot.node(state_name, shape='doublecircle')  #crear un nodo con doble circulo
        else:
            dot.node(state_name)  #crear un nodo simple
        for symbol, states in state.transitions.items():  #iterar sobre las transiciones del estado
            for s in states:  #para cada estado destino
                if s not in seen:  #si el estado destino no ha sido visto
                    visualize(s)  #visualizar el estado destino
                label = escape_label(symbol) if symbol is not None else 'ε'  #preparar la etiqueta de la transicion
                dot.edge(state_name, state_names[s], label=label)  #crear una arista en el grafo con la etiqueta

    visualize(automaton.start_state)  
    all_graphs.append(dot.source)  

def process_yalex_file(input_path, output_path):  
    all_graphs = []  #lista para almacenar todos los grafos generados
    with open(input_path, 'r') as file:  
        for line in file:  
            if ':=' in line:  #si la linea contiene la asignacion de token a regex
                token_name, regex = line.split(':=')  #separar el nombre del token y la regex
                afn = regex_to_afn(regex.strip())  #convertir la regex a un AFN
                if afn:  #si se creo un AFN
                    afd = afn_to_afd(afn)  #convertir el AFN a AFD
                    visualize_automaton(afd, token_name, all_graphs)  #visualizar el AFD y agregarlo a la lista de grafos
                else:  #si hubo un error al crear el AFN
                    print(f"Error al generar el AFN para el token: {token_name}")  
    with open(output_path, 'w', encoding='utf-8') as f: 
        f.write("\n".join(all_graphs))  #escribir todos los grafos en el archivo

def main(input_path, output_path): 
    process_yalex_file(input_path, output_path) 