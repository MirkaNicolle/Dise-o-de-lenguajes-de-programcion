from Thompson import State
from arbol import build_tree  # Asumimos que esta función devuelve un árbol sintáctico con métodos de cálculo de posición
import graphviz

class AFD:
    def __init__(self, start_state):
        self.start_state = start_state
        self.states = [start_state]

    def add_state(self, state):
        if state not in self.states:
            self.states.append(state)

def find_node_by_position(node, position):
    # Si el nodo actual tiene la posición buscada, retornarlo
    if node.position == position:
        return node
    # De lo contrario, buscar recursivamente en los nodos hijos
    found_node = None
    if node.leftnode:
        found_node = find_node_by_position(node.leftnode, position)
        if found_node:
            return found_node
    if node.rightnode:
        found_node = find_node_by_position(node.rightnode, position)
        if found_node:
            return found_node
    return found_node

def build_direct_afd(root):
    # Calcular los conjuntos de posición iniciales del árbol sintáctico
    root.set_positions()

    # Las posiciones iniciales determinan el estado inicial del AFD
    initial_positions = frozenset(root.firstposition)
    print(f"Initial positions: {initial_positions}")
    
    # El estado inicial se determina si está en las últimas posiciones de la raíz
    start_state = State(accept=0 in root.lastposition)
    afd = AFD(start_state)

    # Diccionario para seguir los estados ya creados
    states = {initial_positions: start_state}
    # Lista de estados por procesar
    process = [initial_positions]

    # Procesar todos los estados pendientes
    while process:
        current_positions = process.pop()
        print(f"Processing state with positions: {current_positions}")
        current_state = states[current_positions]

        # Diccionario para mantener las transiciones agrupadas por símbolo
        transitions = {}
        for pos in current_positions:
            node = find_node_by_position(root, pos)
            if not node:
                print(f"No node found for position: {pos}")
                continue
            print(f"Node {node.char} at position {pos} has next positions: {node.nextposition}")
            for symbol, next_positions in node.nextposition.items():
                if symbol in transitions:
                    transitions[symbol].update(next_positions)
                else:
                    transitions[symbol] = set(next_positions)

        print(f"Transitions from state {current_positions}: {transitions}")
        for symbol, next_positions in transitions.items():
            next_positions_frozenset = frozenset(next_positions)
            if next_positions_frozenset not in states:
                accept = any(pos in root.lastposition for pos in next_positions_frozenset)
                new_state = State(accept)
                states[next_positions_frozenset] = new_state
                afd.add_state(new_state)
                process.append(next_positions_frozenset)
            current_state.add_transition(symbol, states[next_positions_frozenset])

    return afd

def visualize_afd(afd):
    dot = graphviz.Digraph(format='png')
    seen = set()
    state_names = {}

    def visualize(state):
        if state in seen:
            return
        seen.add(state)
        state_name = 'S' + str(len(seen))
        state_names[state] = state_name
        if state.accept:
            dot.node(state_name, shape='doublecircle')
        else:
            dot.node(state_name)
        for symbol, states in state.transitions.items():
            for s in states:
                if s not in seen:
                    visualize(s)
                dot.edge(state_name, state_names[s], label=symbol)

    visualize(afd.start_state)
    dot.render('Direct AFD', view=True)

def main():
    with open('postfix.txt', 'r') as file:
        postfix_expr = file.read().strip()

    # Construir el árbol sintáctico
    syntax_tree = build_tree(postfix_expr)
    
    # Asegúrate de que el árbol tiene sus posiciones calculadas
    syntax_tree.set_positions()

    # Construir AFD directamente desde el árbol sintáctico
    afd = build_direct_afd(syntax_tree)

    # Visualizar el AFD
    visualize_afd(afd)

if __name__ == "__main__":
    main()
