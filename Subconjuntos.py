'''Construccion de subconjuntos es un método para convertir un Autómata Finito No Determinista (AFN) en un Autómata Finito Determinista (AFD)
Para cada nuevo estado del AFD se determina el conjunto de estados alcanzables desde cualquier estado en el conjunto actual al consumir el símbolo
Si el conjunto resultante es nuevo, se agrega como un nuevo estado en el AFD.'''

from Thompson import regex_to_afn, AFN, State
import graphviz

'''manejo de epsilon'''
def epsilon_closure(states):
    stack = list(states)  #inicia una pila con los estados iniciales
    closure = set(states)  #crea un conjunto para el cierre epsilon
    while stack:  #mientras la pila no esté vacía
        state = stack.pop()  #extrae un estado de la pila
        if None in state.transitions:  #si hay transiciones epsilon para el estado
            for next_state in state.transitions[None]:  #itera sobre cada estado alcanzable por epsilon
                if next_state not in closure:  #si el estado no está ya en el cierre
                    closure.add(next_state)  #añade el estado al cierre
                    stack.append(next_state)  #apila el estado para su procesamiento
    return closure  #retorna el cierre epsilon de los estados

def move(states, symbol):
    next_states = set()  #conjunto para los proximos estados
    for state in states:  #para cada estado en el conjunto actual
        if symbol in state.transitions:  #si el simbolo está en las transiciones del estado
            next_states.update(state.transitions[symbol])  #añade los estados destino al conjunto
    return next_states  #retorna el conjunto de estados alcanzables por el símbolo

'''conversion afn a afd'''
def afn_to_afd(afn):
    initial_closure = epsilon_closure([afn.start_state])  #obtiene el cierre epsilon del estado inicial
    unmarked = [initial_closure]  #lista de cierres no marcados
    afd_states = {frozenset(initial_closure): State(any(s.accept for s in initial_closure))}  #diccionario de estados del afd
    afd = AFN(afd_states[frozenset(initial_closure)])  #crea el afd

    while unmarked:  #mientras haya cierres no marcados
        current = unmarked.pop()  #obtiene un cierre no marcado
        for symbol in set(sym for state in current for sym in state.transitions if sym is not None):  #para cada símbolo en las transiciones de los estados en el cierre
            move_closure = epsilon_closure(move(current, symbol))  #obtiene el cierre epsilon de los estados alcanzados por el símbolo
            frozenset_closure = frozenset(move_closure)  #hace un conjunto inmutable del cierre
            if frozenset_closure not in afd_states:  #si el cierre no está en los estados del afd
                afd_states[frozenset_closure] = State(any(s.accept for s in move_closure))  #crea un nuevo estado en el afd
                unmarked.append(move_closure)  #marca el nuevo cierre para procesamiento
                afd.add_state(afd_states[frozenset_closure])  #añade el nuevo estado al afd
            afd_states[frozenset(current)].add_transition(symbol, afd_states[frozenset_closure])  #añade la transición en el afd
    return afd  # retorna el afd

def visualize_automaton(automaton, filename='Automaton'):
    dot = graphviz.Digraph(format='png')  #crea un grafico dirigido para visualizacion
    seen = set()  #conjunto de estados ya visualizados
    state_names = {}  #diccionario de nombres de estados
    
    def visualize(state):
        if state in seen:  #si el estado ya fue visualizado, retorna
            return
        seen.add(state)  #marca el estado como visualizado
        state_name = f'S{len(seen)}'  #asigna un nombre al estado
        state_names[state] = state_name  #guarda el nombre del estado
        if state.accept:  #si el estado es de aceptación
            dot.node(state_name, shape='doublecircle')  #visualiza como un doble círculo
        else:
            dot.node(state_name)  #visualiza como un circulo normal
        for symbol, states in state.transitions.items():  
            for s in states:  #para cada estado destino en la transición
                if s not in seen:  #si el estado destino no ha sido visualizado
                    visualize(s)  #visualizacion del estado destino
                dot.edge(state_name, state_names[s], label=symbol if symbol else 'ε')  #añade una arista al grafico
    
    visualize(automaton.start_state) 
    dot.render(filename, view=True)  

def main():
    with open('postfix.txt', 'r') as file:  
        postfix_regex = file.read().strip()  
    afn = regex_to_afn(postfix_regex)  #conversion a afd
    if afn: 
        afd = afn_to_afd(afn)  #convierte el afn a afd
        visualize_automaton(afd, 'Subconjuntos AFD')
    else: 
        print("error al generar el afn")

if __name__ == '__main__':
    main()