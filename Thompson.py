'''Thompson es un método que convierte una expresión regular en un Autómata Finito No Determinista (AFN)'''

import graphviz

class State:  
    def __init__(self, accept=False): 
        self.accept = accept  
        self.transitions = {}  #diccionario de transiciones

    def add_transition(self, symbol, state):  #agregar una transicion
        if symbol in self.transitions:  #si el simbolo ya esta en las transiciones
            self.transitions[symbol].append(state)  #agregar el estado a la lista de transiciones bajo ese simbolo
        else:
            self.transitions[symbol] = [state]  #crear una nueva entrada en el diccionario para el simbolo con una lista que contiene el estado

class AFN: 
    def __init__(self, start_state): 
        self.start_state = start_state 
        self.states = [start_state]  #inicializar lista de estados con el estado inicial

def regex_to_afn(postfix_regex): 
    stack = []  #pila para construccion de afn
    i = 0  #contador para iterar a traves del regex
    while i < len(postfix_regex):  #iterar mientras haya caracteres en la regex
        char = postfix_regex[i]  #obtener el caracter actual
        if char.isalnum() or char in ('.', '_'):  #si el caracter es alfanumerico o uno de esos caracteres
            start = State()  #crear un nuevo estado inicial
            end = State(True)  #crear un nuevo estado final con aceptacion
            start.add_transition(char, end)  #agregar una transicion directa del inicio al fin con el caracter
            stack.append((start, end))  #agregar la pareja de estados a la pila
        elif char == '[':  #si es un inicio de clase de caracteres
            start = State()  #nuevo estado inicial
            end = State(True)  #nuevo estado final con aceptacion
            i += 1  #avanzar al siguiente caracter
            char_class = []  #inicializar la lista de caracteres en la clase
            while postfix_regex[i] != ']':  #hasta encontrar el cierre de la clase
                if postfix_regex[i] == '\\':  #si hay una secuencia de escape
                    i += 1  #avanzar al caracter escapado
                char_class.append(postfix_regex[i])  #agregar el caracter a la lista de la clase
                i += 1  
            start.add_transition("".join(char_class), end)  #agregar la transicion con la clase de caracteres unida como cadena
            stack.append((start, end))  #agregar la pareja a la pila
            i += 1  
        elif char in ['*', '+']:  #si es un operador de clausura o positiva
            afn = stack.pop()  #sacar la pareja de estados de la pila
            start = State()  #nuevo estado inicial
            end = State(True)  #nuevo estado final con aceptacion
            start.add_transition(None, afn[0])  #transicion epsilon del nuevo inicio al inicio del afn extraido
            afn[1].add_transition(None, end)  #transicion epsilon del fin del afn extraido al nuevo fin
            if char == '*':  #si es una clausura de Kleene
                start.add_transition(None, end)  #agregar una transicion epsilon directa del inicio al fin
            afn[1].add_transition(None, afn[0])  #transicion epsilon del fin al inicio del afn para repetir
            stack.append((start, end))  #agregar la nueva pareja de estados a la pila
        i += 1  

    if stack:  #si hay algo en la pila al finalizar
        afn = stack.pop()  #obtener la ultima pareja de estados
        return AFN(afn[0])  #retornar el AFN creado con el estado inicial de la pareja
    return None  #retornar None si no se pudo crear un AFN

def visualize_afn(afn, token_name, all_graphs):  
    dot = graphviz.Digraph(name=f"digraph_afn_{token_name}") 
    seen = set()  #conjunto para rastrear los estados ya vistos
    state_names = {}  #diccionario para asignar nombres a los estados

    def escape_label(text):  #funcion para evitar etiquetas
        return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')  #evita caracteres especiales

    def visualize(state):  
        if state in seen:  #si el estado ya fue visualizado
            return
        seen.add(state)  #marcar el estado como visto
        state_name = 'S' + str(len(seen))  #asignar un nombre al estado basado en el orden de visualizacion
        state_names[state] = state_name  #guardar el nombre asignado al estado
        if state.accept:  #si el estado es de aceptacion
            dot.node(state_name, shape='doublecircle')  #crea un nodo con doble circulo
        else:
            dot.node(state_name)  #crea un nodo simple
        for symbol, states in state.transitions.items():  #iterar sobre las transiciones del estado
            for s in states:  #para cada estado destino
                if s not in seen:  #si el estado destino no ha sido visto
                    visualize(s)  #visualizar el estado destino
                label = escape_label(symbol) if symbol is not None else 'ε'  #prepara la etiqueta de la transicion
                dot.edge(state_name, state_names[s], label=label)  #crea una arista en el grafo con la etiqueta

    visualize(afn.start_state)  #comenzar la visualizacion desde el estado inicial
    all_graphs.append(dot.source)  #agregar la fuente del grafo a la lista de todos los grafos

def process_yalex_file(input_path, output_path):  
    all_graphs = []  #lista para almacenar todos los grafos generados
    with open(input_path, 'r', encoding='utf-8') as file: 
        for line in file:  #leer linea por linea
            if ':=' in line:  #si la linea contiene la asignacion de token a regex
                token_name, regex = line.split(':=')  #separar el nombre del token y la regex
                afn = regex_to_afn(regex.strip())  #convertir la regex a un AFN
                if afn:  #si se creo un AFN
                    visualize_afn(afn, token_name, all_graphs)  #visualizar el AFN y agregarlo a la lista de grafos
                else:  #si hubo un error al crear el AFN
                    print(f"Error al generar el AFN para el token: {token_name}") 
    with open(output_path, 'w', encoding='utf-8') as f:  
        f.write("\n".join(all_graphs))  #escribir todos los grafos en el archivo

def main(input_path, output_path):  
    process_yalex_file(input_path, output_path)  