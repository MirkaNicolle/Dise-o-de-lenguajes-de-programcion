'''El algoritmo de minimización para Autómatas Finitos Deterministas (AFD), reduce el número de estados al mínimo necesario para reconocer el mismo lenguaje'''

from Thompson import regex_to_afn, State, AFN
from Subconjuntos import visualize_automaton, afn_to_afd
import graphviz

def remove_unreachable_states(afd):
    reachable = set()  #conjunto de estados alcanzables
    stack = [afd.start_state]  #pila iniciada con el estado de inicio
    while stack:  #mientras haya estados en la pila
        state = stack.pop()  #extrae un estado de la pila
        if state not in reachable:  #si el estado no esta marcado como alcanzable
            reachable.add(state)  #marca el estado como alcanzable
            for symbol in state.transitions:  #para cada simbolo en las transiciones del estado
                stack.extend(state.transitions[symbol])  #adicion los estados destino a la pila

    afd.states = [state for state in afd.states if state in reachable]  #filtra los estados no alcanzables

'''minimizacion de afd'''
def minimize_afd(afd):
    remove_unreachable_states(afd)  #elimina estados no alcanzables

    P = {frozenset([s for s in afd.states if s.accept]), frozenset([s for s in afd.states if not s.accept])} #inicializacion de los conjuntos de estados aceptacion y no aceptacion
    B = set(P)  #conjuntos de trabajo, inicialmente igual a P

    while B:  #mientras haya elementos en B
        A = B.pop()  #toma un conjunto de B
        for symbol in set(sym for state in A for sym in state.transitions):  #para cada simbolo de las transiciones de A
            C = set(s for s in A if symbol in s.transitions and set(s.transitions[symbol]) & A)  #estados de A con transiciones por el simbolo que quedan en A
            for D in P.copy():  
                intersect = C & D  #interseccion de C y D
                difference = D - C  #diferencia de D y C
                if intersect and difference:  #si ambos subconjuntos son no vacios
                    P.remove(D)  #elimina el conjunto viejo
                    P.add(frozenset(intersect))  #adicion a la interseccion como nuevo conjunto
                    P.add(frozenset(difference))  #adicion a la diferencia como nuevo conjunto
                    if D in B:
                        B.remove(D)  #actualiza B removiendo el conjunto viejo
                        B.add(frozenset(intersect))  #adicion a los nuevos conjuntos a B
                        B.add(frozenset(difference))
                    else:
                        B.add(frozenset(intersect) if len(intersect) <= len(difference) else frozenset(difference)) #adicion al subconjunto mas pequeño a B

    new_states = {frozenset(group): State(any(s.accept for s in group)) for group in P} #crea nuevos estados para el afd minimizado
    start_state = next(new_states[frozenset(group)] for group in P if afd.start_state in group)  #estado inicial del afd minimizado

    for group, new_state in new_states.items(): #reconstruccion de transiciones sin duplicar
        for symbol in set(sym for state in group for sym in state.transitions):
            target_set = set()
            for state in group:
                if symbol in state.transitions:
                    for target in state.transitions[symbol]:
                        target_group = next(g for g in P if target in g)
                        target_set.add(new_states[frozenset(target_group)])

            for target in target_set:
                new_state.add_transition(symbol, target)  #añade una unica transicion a cada estado destino

    return AFN(start_state)

def visualize_automaton(automaton, filename='Automaton'):
    dot = graphviz.Digraph(format='png')
    seen = set()  #conjunto de estados ya visitados
    state_names = {}

    def visualize(state):
        if state in seen:
            return  #si el estado ya fue visitado, retorna
        seen.add(state)  #marca el estado como visualizado o visitado
        state_name = f'S{len(seen)}'  #asigna un nombre al estado
        state_names[state] = state_name  #guarda el nombre del estado
        if state.accept:
            dot.node(state_name, shape='doublecircle')
        else:
            dot.node(state_name)  #visualiza como un circulo normal
        for symbol, states in state.transitions.items():
            for s in states:
                if s not in seen:
                    visualize(s)  #visualiza el estado destino
                dot.edge(state_name, state_names[s], label=symbol if symbol else 'ε') #añade una arista al grafo

    visualize(automaton.start_state)
    dot.render(filename, view=True)  

def main():
    with open('postfix.txt', 'r') as file:
        postfix_regex = file.read().strip() 
    afn = regex_to_afn(postfix_regex)
    if afn:
        afd = afn_to_afd(afn) 
        minimized_afd = minimize_afd(afd)
        visualize_automaton(minimized_afd, 'Minimizacion AFD') 
    else:
        print("error al generar el afn")  

if __name__ == '__main__':
    main()  