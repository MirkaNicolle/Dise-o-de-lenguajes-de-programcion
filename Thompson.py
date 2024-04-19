'''Thompson es un método que convierte una expresión regular en un Autómata Finito No Determinista (AFN)'''

import graphviz

class State:
    def __init__(self, accept=False):
        self.accept = accept
        self.transitions = {}

    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]

class AFN:
    def __init__(self, start_state):
        self.start_state = start_state  # Estado inicial del AFN
        self.states = [start_state]     # Lista de estados que comienza con el estado inicial

    def add_state(self, state):
        if state not in self.states:
            self.states.append(state)   # Añade un nuevo estado a la lista de estados si aún no está presente

    def add_transition(self, from_state, to_state, symbol):
        # Asegúrate de que tanto from_state como to_state estén en self.states
        if from_state in self.states and to_state in self.states:
            from_state.add_transition(symbol, to_state)  # Añade la transición usando el método definido en la clase State

def regex_to_afn(postfix_regex):
    stack = []
    i = 0
    while i < len(postfix_regex):
        char = postfix_regex[i]
        if char.isalnum():  # Manejo simple de caracteres alfanuméricos
            start = State()
            end = State(True)
            start.add_transition(char, end)
            stack.append((start, end))
        elif char == '[':  # Inicio de una clase de caracteres
            start = State()
            end = State(True)
            i += 1
            char_class = []
            while postfix_regex[i] != ']':
                if postfix_regex[i] == '\\':  # Escape dentro de la clase
                    i += 1
                char_class.append(postfix_regex[i])
                i += 1
            start.add_transition("".join(char_class), end)
            stack.append((start, end))
            i += 1  # Moverse más allá del ']' para continuar procesamiento
        elif char in ['*', '+']:  # Operadores de repetición
            afn = stack.pop()
            start = State()
            end = State(True)
            start.add_transition(None, afn[0])
            afn[1].add_transition(None, end)
            if char == '*':
                start.add_transition(None, end)
            afn[1].add_transition(None, afn[0])
            stack.append((start, end))
        i += 1

    if stack:
        afn = stack.pop()
        return AFN(afn[0])
    return None

def visualize_afn(afn, token_name):
    dot = graphviz.Digraph(format='png')
    seen = set()
    state_names = {}

    def escape_label(text):
        return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

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
                label = escape_label(symbol) if symbol is not None else 'ε'
                dot.edge(state_name, state_names[s], label=label)

    visualize(afn.start_state)
    dot.render(f'Thompson_AFN_{token_name}', view=True)

def process_yalex_file(input_path):
    with open(input_path, 'r') as file:
        for line in file:
            if ':=' in line:
                token_name, regex = line.split(':=')
                afn = regex_to_afn(regex.strip())
                if afn:
                    visualize_afn(afn, token_name)
                else:
                    print(f"Error al generar el AFN para el token: {token_name}")

def main():
    process_yalex_file('output_postfix.yalex')

if __name__ == '__main__':
    main()