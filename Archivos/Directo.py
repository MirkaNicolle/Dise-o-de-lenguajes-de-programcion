'''Este metodo construye el AFD directamente a partir de una expresion regular analizada, utilizando la estructura de un arbol sintactico'''

from Thompson import State
from arbol import build_tree
import graphviz

class AFD:
    def __init__(self, start_state):
        self.start_state = start_state  #establece el estado inicial del afd
        self.states = [start_state]  #inicializa la lista de estados con el estado inicial

    def add_state(self, state):
        if state not in self.states:  #verifica si el estado no está ya en la lista de estados
            self.states.append(state)  #añade el estado a la lista de estados del afd

def find_node_by_position(node, position):
    if node.position == position: #si el nodo actual tiene la posicion buscada, retornarlo
        return node
    found_node = None #de lo contrario, buscar recursivamente en los nodos hijos
    if node.leftnode:
        found_node = find_node_by_position(node.leftnode, position)  #busca en el hijo izquierdo
        if found_node:
            return found_node
    if node.rightnode:
        found_node = find_node_by_position(node.rightnode, position)  #busca en el hijo derecho
        if found_node:
            return found_node
    return found_node  #retorna el nodo encontrado o None si no se encuentra

'''contruccion de afd directo'''
def build_direct_afd(root):
    root.set_positions() #calcular los conjuntos de posicion iniciales del arbol sintactico

    initial_positions = frozenset(root.firstposition) #las posiciones iniciales determinan el estado inicial del afd
    #print(f"Initial positions: {initial_positions}") 
    
    start_state = State(accept=0 in root.lastposition) #el estado inicial se determina si esta en las ultimas posiciones de la raiz
    afd = AFD(start_state)  #crea un afd con el estado inicial

    states = {initial_positions: start_state} #diccionario para seguir los estados ya creados
    process = [initial_positions] #lista de estados por procesar

    while process: #procesar todos los estados pendientes
        current_positions = process.pop()  #toma el conjunto actual de posiciones
        #print(f"Processing state with positions: {current_positions}")
        current_state = states[current_positions]

        transitions = {} #diccionario para mantener las transiciones agrupadas por simbolo
        for pos in current_positions:
            node = find_node_by_position(root, pos)  #encuentra el nodo por posicion
            if not node:
                #print(f"No node found for position: {pos}")
                continue
            #print(f"Node {node.char} at position {pos} has next positions: {node.nextposition}")
            for symbol, next_positions in node.nextposition.items():
                if symbol in transitions:
                    transitions[symbol].update(next_positions)  #actualiza el conjunto de posiciones para el simbolo
                else:
                    transitions[symbol] = set(next_positions)  #crea un nuevo conjunto de posiciones para el simbolo

        #print(f"Transitions from state {current_positions}: {transitions}")
        for symbol, next_positions in transitions.items():
            next_positions_frozenset = frozenset(next_positions)
            if next_positions_frozenset not in states:
                accept = any(pos in root.lastposition for pos in next_positions_frozenset)
                new_state = State(accept)
                states[next_positions_frozenset] = new_state  #añade el nuevo estado al diccionario de estados
                afd.add_state(new_state)  #añade el nuevo estado al afd
                process.append(next_positions_frozenset)
            current_state.add_transition(symbol, states[next_positions_frozenset])  #añade una transicion al estado actual

    return afd  # retorna el afd construido

def visualize_afd(afd):
    dot = graphviz.Digraph(format='png')
    seen = set()  #conjunto de estados ya visualizados
    state_names = {}

    def visualize(state):
        if state in seen:
            return  #si el estado ya fue visualizado, retorna
        seen.add(state)  #marca el estado como visualizado
        state_name = 'S' + str(len(seen))  #genera un nombre para el estado
        state_names[state] = state_name  #asigna el nombre al estado
        if state.accept:
            dot.node(state_name, shape='doublecircle')  #visualiza como un doble circulo si es de aceptacion
        else:
            dot.node(state_name)  #visualiza como un circulo normal si no es de aceptacion
        for symbol, states in state.transitions.items():
            for s in states:
                if s not in seen:
                    visualize(s)  #visualiza el estado destino si no ha sido visualizado
                dot.edge(state_name, state_names[s], label=symbol)  #añade una arista al grafo

    visualize(afd.start_state)  #visualizacion del grafo
    dot.render('AFD Directo', view=True)  

def main():
    with open('postfix.txt', 'r') as file:
        postfix_expr = file.read().strip()

    syntax_tree = build_tree(postfix_expr) #construccion de el árbol sintáctico
    syntax_tree.set_positions()
    
    afd = build_direct_afd(syntax_tree) #creacion de afd directo

    visualize_afd(afd)

if __name__ == "__main__":
    main()
