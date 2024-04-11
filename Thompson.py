import graphviz

class State:
    """
    Representa un estado dentro de un AFN. 
    Cada estado puede tener múltiples transiciones a otros estados.
    """
    def __init__(self, accept=False):
        self.accept = accept  # Indica si el estado es de aceptación.
        self.transitions = {}  # Diccionario para transiciones: clave = símbolo, valor = lista de estados destino.

    def add_transition(self, symbol, state):
        """
        Añade una transición desde este estado a otro estado dado un símbolo.
        """
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]

class NFA:
    """
    Representa un Autómata Finito No Determinista (AFN).
    """
    def __init__(self, start_state):
        self.start_state = start_state  # Estado inicial del AFN
        self.states = [start_state]

    def add_state(self, state):
        self.states.append(state)

def regex_to_nfa(postfix_regex):
    """
    Convierte una expresión regular en notación postfija a un AFN utilizando el algoritmo de McNaughton-Yamada-Thompson.
    """
    stack = []
    state_id = 1  # Iniciar los IDs de estado desde 1.

    for char in postfix_regex:
        if char.isalnum():  # Símbolo
            start = State()
            end = State(True)
            start.add_transition(char, end)
            stack.append((start, end))
        elif char == '|':  # Unión
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State()
            end = State(True)
            start.add_transition(None, nfa1[0])
            start.add_transition(None, nfa2[0])
            nfa1[1].accept = False
            nfa2[1].accept = False
            nfa1[1].add_transition(None, end)
            nfa2[1].add_transition(None, end)
            stack.append((start, end))
        elif char == '.' or char == '•':  # Concatenación (modificado para reconocer •)
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1[1].accept = False
            nfa1[1].add_transition(None, nfa2[0])
            stack.append((nfa1[0], nfa2[1]))
        elif char == '*':  # Cierre de Kleene
            nfa = stack.pop()
            start = State()
            end = State(True)
            start.add_transition(None, nfa[0])
            start.add_transition(None, end)
            nfa[1].accept = False
            nfa[1].add_transition(None, nfa[0])
            nfa[1].add_transition(None, end)
            stack.append((start, end))

    if stack:
        nfa = stack.pop()
        return NFA(nfa[0])
    return None

def visualize_nfa(nfa):
    dot = graphviz.Digraph(format='png')
    seen = set()
    state_names = {}

    def visualize(state):
        if state in seen:
            return
        seen.add(state)
        # Asignar un nombre secuencial más simple a cada estado antes de procesar las transiciones
        state_name = 'S' + str(len(seen))
        state_names[state] = state_name
        if state.accept:
            dot.node(state_name, shape='doublecircle')
        else:
            dot.node(state_name)
        for symbol, states in state.transitions.items():
            for s in states:
                # Asegurar que el estado destino también sea procesado y añadido a state_names
                if s not in seen:
                    visualize(s)
                label = symbol if symbol is not None else 'ε'
                dot.edge(state_name, state_names[s], label=label)

    visualize(nfa.start_state)
    dot.render('NFA Thompson', view=True)

def main():
    with open('postfix.txt', 'r') as file:
        postfix_regex = file.read().strip()
    nfa = regex_to_nfa(postfix_regex)
    if nfa:
        visualize_nfa(nfa)
    else:
        print("Error al generar el NFA.")

if __name__ == '__main__':
    main()