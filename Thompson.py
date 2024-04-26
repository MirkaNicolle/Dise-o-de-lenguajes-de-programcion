'''Thompson es un método que convierte una expresión regular en un Autómata Finito No Determinista (AFN)'''

import graphviz

class State:
    def __init__(self, accept=False):
        self.accept = accept  #estado acepta si es verdadero
        self.transitions = {}  #diccionario de transiciones

    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)  #agregar estado a la transicion existente
        else:
            self.transitions[symbol] = [state]  #crear nueva transicion para el simbolo

class AFN:
    def __init__(self, start_state):
        self.start_state = start_state  #estado inicial del afn
        self.states = [start_state]     #lista de estados comienza con el estado inicial

    def add_state(self, state):
        if state not in self.states:
            self.states.append(state)   #anadir nuevo estado si no esta presente

    def add_transition(self, from_state, to_state, symbol):
        if from_state in self.states and to_state in self.states:
            from_state.add_transition(symbol, to_state)  #anadir transicion entre estados

def regex_to_afn(postfix_regex):
    stack = []  #pila para construccion de afn
    i = 0  #indice para iterar a traves del regex
    while i < len(postfix_regex):
        char = postfix_regex[i]  #caracter actual del regex
        print(f"Processing character: {char}")  #imprime el caracter actual para depuracion

        if char.isalnum():  #si el caracter es alfanumerico
            start = State()  #crea un nuevo estado inicial sin aceptacion
            end = State(True)  #crea un nuevo estado final con aceptacion
            start.add_transition(char, end)  #agrega una transición desde el estado inicial al final usando el caracter actual
            stack.append((start, end))  #añade la pareja de estados (inicio, fin) a la pila para gestionar el AFN
            print(f"Added basic transition for {char}")  #imprime transicion basica agregada

        elif char == '[':  #inicio de clase de caracteres
            start = State()  #crea un nuevo estado inicial sin aceptacion
            end = State(True)  #crea un nuevo estado final con aceptacion
            i += 1  #avanza al siguiente caracter en la expresion
            char_class = []  #lista para acumular caracteres de la clase
            while postfix_regex[i] != ']':  #continua hasta el fin de la clase de caracteres
                if postfix_regex[i] == '\\':  #maneja escape dentro de la clase
                    i += 1  #salta el caracter para obtener el siguiente
                char_class.append(postfix_regex[i])  #agrega el caracter a la lista de la clase
                i += 1  #avanza al siguiente caracter
            start.add_transition("".join(char_class), end)  #agrega una transicion con todos los caracteres de la clase
            stack.append((start, end))  #apila el par de estados (inicio, fin)
            print(f"Added class transition: {''.join(char_class)}")  #imprime transicion de clase agregada
            i += 1  #avanza al siguiente caracter despues del cierre de la clase

        elif char in ['*', '+']:  #operadores de clausura y positiva
            afn = stack.pop()  #saca el ultimo par de estados de la pila
            start = State()  #crea un nuevo estado inicial
            end = State(True)  #crea un nuevo estado final
            start.add_transition(None, afn[0])  #agrega transicion epsilon del nuevo inicio al inicio del afn extraido
            afn[1].add_transition(None, end)  #agrega transicion epsilon del fin del afn extraido al nuevo fin
            if char == '*':  #si es una clausura de kleene
                start.add_transition(None, end)  #agrega transicion epsilon directa del inicio al fin
            afn[1].add_transition(None, afn[0])  #agrega transicion epsilon del fin al inicio para repetir
            stack.append((start, end))  #apila la nueva pareja de estados
            print(f"Added repetition {char}")  #imprime operador de repeticion agregado
        i += 1  #avanza al siguiente caracter

    if stack:
        afn_tuple = stack.pop()
        afn = AFN(afn_tuple[0])  #crea afn con el estado inicial de la tupla
        print(f"Final AFN created with start state {id(afn.start_state)}")  #imprime estado inicial del afn final
        return afn

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