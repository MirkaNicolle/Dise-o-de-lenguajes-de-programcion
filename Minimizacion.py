'''El algoritmo de minimización para Autómatas Finitos Deterministas (AFD), reduce el número de estados al mínimo necesario para reconocer el mismo lenguaje'''

from Thompson import regex_to_afn, State, AFN
from Subconjuntos import visualize_automaton, afn_to_afd
import graphviz

def remove_unreachable_states(afd):  #eliminar estados inalcanzables de un afd
    reachable = set()  #inicializar conjunto de estados alcanzables
    stack = [afd.start_state]  #iniciar pila con el estado inicial
    while stack:  #mientras la pila no este vacia
        state = stack.pop()  #extraer estado de la pila
        if state not in reachable:  #si el estado no esta en el conjunto de alcanzables
            reachable.add(state)  #agregar estado a alcanzables
            for symbol in state.transitions:  #iterar sobre cada simbolo de transicion del estado
                stack.extend(state.transitions[symbol])  #agregar estados de destino a la pila
    afd.states = [state for state in afd.states if state in reachable]  #filtrar estados del afd a solo alcanzables

def minimize_afd(afd):  #definir funcion para minimizar un afd
    remove_unreachable_states(afd)  #primero remover estados inalcanzables
    P = {frozenset([s for s in afd.states if s.accept]), frozenset([s for s in afd.states if not s.accept])}  #particion inicial de estados
    B = set(P)  #conjunto de bloques a revisar

    while B:  #mientras haya bloques por revisar
        A = B.pop()  #sacar un bloque de estados
        for symbol in set(sym for state in A for sym in state.transitions):  #para cada simbolo en las transiciones de estados en A
            C = set(s for s in A if symbol in s.transitions and set(s.transitions[symbol]) & A)  #estados en A con transiciones por el simbolo hacia A
            for D in P.copy():  #para cada bloque en la particion actual
                intersect = C & D  #interseccion de C y D
                difference = D - C  #diferencia de D y C
                if intersect and difference:  #si ambos no son vacios
                    P.remove(D)  #remover D de la particion
                    P.add(frozenset(intersect))  #agregar interseccion como nuevo bloque
                    P.add(frozenset(difference))  #agregar diferencia como nuevo bloque
                    if D in B:  #si D estaba en bloques a revisar
                        B.remove(D)  #remover D
                        B.add(frozenset(intersect))  #agregar interseccion
                        B.add(frozenset(difference))  #agregar diferencia
                    else:
                        B.add(frozenset(intersect) if len(intersect) <= len(difference) else frozenset(difference))  #agregar bloque mas pequeno
    
    new_states = {frozenset(group): State(any(s.accept for s in group)) for group in P}  #crear nuevos estados por cada bloque
    start_state = next(new_states[frozenset(group)] for group in P if afd.start_state in group)  #determinar el nuevo estado inicial
    for group, new_state in new_states.items():  #para cada grupo y su estado correspondiente
        for symbol in set(sym for state in group for sym in state.transitions):  #para cada simbolo en transiciones de estados en el grupo
            target_set = set()  #conjunto de estados destino
            for state in group:  #para cada estado en el grupo
                if symbol in state.transitions:  #si hay transicion por el simbolo
                    for target in state.transitions[symbol]:  #para cada estado destino
                        target_group = next(g for g in P if target in g)  #encontrar el grupo del estado destino
                        target_set.add(new_states[frozenset(target_group)])  #agregar estado correspondiente al conjunto destino
            for target in target_set:  #para cada estado destino
                new_state.add_transition(symbol, target)  #agregar transicion al nuevo estado

    return AFN(start_state)  #retornar el AFN con el nuevo estado inicial

def visualize_automaton(automaton, filename='Automaton'): 
    dot = graphviz.Digraph(format='png')  
    seen = set()  #conjunto de estados ya visualizados
    state_names = {}  #diccionario para nombres de estados

    def escape_label(text):  #funcion para escapar etiquetas
        return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('^', '\\^').replace('{', '\\{').replace('}', '\\}')  #escapar caracteres especiales

    def visualize(state):  #funcion para visualizar estados
        if state in seen:  #si el estado ya fue visualizado
            return
        seen.add(state)  #marcar el estado como visto
        state_name = f'S{len(seen)}'  #asignar un nombre al estado
        state_names[state] = state_name  #guardar el nombre del estado
        if state.accept:  #si el estado es de aceptacion
            dot.node(state_name, shape='doublecircle')  #crear un nodo con doble circulo
        else:
            dot.node(state_name)  #crear un nodo simple
        for symbol, states in state.transitions.items():  #para cada simbolo y sus estados destino
            for s in states:  #para cada estado destino
                if s not in seen:  #si el estado no ha sido visto
                    visualize(s)  #visualizar el estado destino
                label = escape_label(symbol) if symbol is not None else 'ε'  
                dot.edge(state_name, state_names[s], label=label)  #crear una arista con la etiqueta

    visualize(automaton.start_state)  #visualizar el estado inicial
    dot.render(filename, view=True)  #renderizar y guardar el grafico