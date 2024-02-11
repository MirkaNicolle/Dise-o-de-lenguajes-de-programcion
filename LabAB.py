'''
Laboratorio AB
Lenguajes de programación   
9 de febrero de 2024
'''
import networkx as nx
import matplotlib.pyplot as plt

class Automaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        # Inicializa un objeto Automaton con estados, alfabeto, transiciones, estado inicial y estados de aceptación.
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

#clase nodo, caracteristicas
class Node:
    def __init__(self, char, position=None, nullable=None):
        self.char = char
        self.position = position
        self.firstposition = {position}
        self.lastposition = {position}
        self.nextposition = set()
        self.nullable = nullable
        self.leftnode = None
        self.rightnode = None

    def setPositions(self):
        if self.rightnode:
            self.rightnode.setPositions()
        if self.leftnode:
            self.leftnode.setPositions()
        #aqui van los pasos de carlos
        if self.char == ".":
            self.leftnode #detallar la instruccion

operators = ["*", "|", "."]

def build_tree(expression):
    build = []
    expression = expression.replace(" ","")

    i = 0

    for char in expression:
        if char in operators:
            if char == "*" :
                leftnode = build.pop()
                build.append(Node(char))
                build[-1].leftnode = leftnode
            else:
                rightnode = build.pop()
                leftnode = build.pop()
                build.append(Node(char))
                build[-1].leftnode = leftnode
                build[-1].rightnode = rightnode
        else:
            build.append(Node(char, i+1, False)) #aqui va if char = epsilon: nullable = true else nullable = false
        i += 1

    build[0].setPositions()
    #return build[0] 

def add_concatenation_dot(regex):
    result = []  # Lista para almacenar la nueva expresión con puntos de concatenación
    special_chars = {'|', '*', '(', ')'}  # Caracteres especiales en regex

    for i in range(len(regex) - 1):
        result.append(regex[i])
        # Casos donde se necesita añadir un punto '.'
        if (regex[i] not in special_chars and regex[i + 1] not in special_chars) or \
            (regex[i] not in special_chars and regex[i + 1] == '(') or \
            (regex[i] == ')' and regex[i + 1] not in special_chars) or \
            (regex[i] == '*' and regex[i + 1] not in special_chars) or \
            (regex[i] == '*' and regex[i + 1] == '('):
            result.append('.')

    result.append(regex[-1])  # Añadir el último carácter de la expresión regular
    return ''.join(result)

def shunting_yard(infix_expression):
    parsed_expresion = add_concatenation_dot(infix_expression)
    queue = []
    stack = []

    def get_precende(c):
        if char == "*" : return 3
        if char == "." : return 2
        if char == "|" : return 1
        return 0

    i=0
    for char in parsed_expresion:
        if char.isalnum():
            queue.append(char)
        elif char in operators:
            while (stack and stack[-1] in operators and get_precende(stack[-1]) >= get_precende(char)):
                c = stack.pop()
                queue.append(c)
            stack.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                c=stack.pop()
                queue.append(c)
            c= stack.pop()
        i+=1

    while stack:
        c=stack.pop()
        queue.append(c)
    
    result = ""

    for c in queue:
        result += c
    return result

""" def thompson_algorithm(postfix_expression):
    # Algoritmo Thompson para construir un autómata finito no determinista (AFN)
    stack = []

    for token in postfix_expression:
        if token.isalnum():
            # Si el token es alfanumérico, crea un AFN básico con un estado inicial, un estado de aceptación y una transición entre ellos
            accept_state = 1
            start_state = 0
            transitions = {(start_state, token): {accept_state}}
            afn = Automaton({start_state, accept_state}, {token}, transitions, start_state, {accept_state})
            stack.append(afn)
        elif token == '*':
            # Operación de Cerradura de Kleene: crea un nuevo estado inicial y de aceptación, y conecta con transiciones epsilon al AFN anterior
            operand = stack.pop()
            accept_state = max(operand.accept_states) + 1
            start_state = min(operand.states) - 1
            transitions = operand.transitions.copy()
            transitions.update({(accept_state, None): {operand.start_state}})
            transitions.update({(start_state, None): {accept_state}})
            transitions.update({(operand.accept_states.pop(), None): {operand.start_state}})
            transitions.update({(accept_state, None): {start_state}})
            afn = Automaton(operand.states | {start_state, accept_state}, operand.alphabet, transitions, start_state, {accept_state})
            stack.append(afn)
        elif token == '.':
            # Operación de Concatenación: conecta el estado de aceptación del primer AFN con el estado inicial del segundo AFN
            operand2 = stack.pop()
            operand1 = stack.pop()
            accept_state = max(operand2.accept_states)
            transitions = operand1.transitions.copy()
            transitions.update(operand2.transitions)
            transitions[(operand1.accept_states.pop(), None)].add(operand2.start_state)
            afn = Automaton(operand1.states | operand2.states, operand1.alphabet | operand2.alphabet, transitions, operand1.start_state, {accept_state})
            stack.append(afn)
        elif token == '|':
            # Operación de Unión (OR): crea nuevos estados inicial y de aceptación, y conecta con transiciones epsilon a los estados iniciales de los AFN anteriores
            operand2 = stack.pop()
            operand1 = stack.pop()
            accept_state = max(operand1.accept_states) + max(operand2.accept_states) + 1
            start_state = min(operand1.states) - 1
            transitions = operand1.transitions.copy()
            transitions.update(operand2.transitions)
            transitions.update({(start_state, None): {operand1.start_state, operand2.start_state}})
            transitions.update({(accept_state1, None): {accept_state} for accept_state1 in operand1.accept_states})
            transitions.update({(accept_state2, None): {accept_state} for accept_state2 in operand2.accept_states})
            afn = Automaton(operand1.states | operand2.states | {start_state, accept_state}, operand1.alphabet | operand2.alphabet, transitions, start_state, {accept_state})
            stack.append(afn)

    return stack.pop()

def epsilon_closure(states, transitions):
    # Calcula la cerradura-épsilon de un conjunto de estados en un AFN
    closure = set(states)
    stack = list(states)

    while stack:
        current_state = stack.pop()
        epsilon_moves = transitions.get((current_state, None), set())

        for state in epsilon_moves:
            if state not in closure:
                closure.add(state)
                stack.append(state)

    return frozenset(closure)

def move(states, symbol, transitions):
    # Realiza la operación de moverse desde un conjunto de estados dado un símbolo en un AFN
    result = set()

    for state in states:
        transitions_for_state = transitions.get((state, symbol), set())
        result.update(transitions_for_state)

    return frozenset(result)

def nfa_to_dfa(nfa):
    # Convierte un AFN a un AFD usando el algoritmo de construcción de subconjuntos
    dfa_states = set()
    dfa_transitions = {}
    dfa_start_state = epsilon_closure({nfa.start_state}, nfa.transitions)
    dfa_accept_states = set()

    stack = [dfa_start_state]
    seen = set()

    while stack:
        current_states = stack.pop()
        dfa_states.add(current_states)

        for symbol in nfa.alphabet:
            next_states = epsilon_closure(move(current_states, symbol, nfa.transitions), nfa.transitions)
            dfa_transitions[(current_states, symbol)] = next_states

            if next_states not in seen:
                seen.add(next_states)
                stack.append(next_states)

        if nfa.accept_states.intersection(current_states):
            dfa_accept_states.add(current_states)

    return Automaton(dfa_states, nfa.alphabet, dfa_transitions, dfa_start_state, dfa_accept_states)

def minimize_dfa(dfa):
    # Minimiza un AFD utilizando el algoritmo de particiones
    partition = [dfa.accept_states, dfa.states - dfa.accept_states]

    while True:
        new_partition = []

        for group in partition:
            for symbol in dfa.alphabet:
                next_states = dfa.transitions.get((next(iter(group)), symbol), set())
                next_group = [state for state in partition if next_states.issubset(state)][0]
                new_partition.append(set(next_group))

        if new_partition == partition:
            break
        partition = new_partition

    dfa_minimized_states = set(range(len(partition)))
    dfa_minimized_start_state = next(i for i, group in enumerate(partition) if dfa.start_state in group)
    dfa_minimized_accept_states = {i for i, group in enumerate(partition) if dfa.accept_states.intersection(group)}

    dfa_minimized_transitions = {}
    for group in partition:
        for symbol in dfa.alphabet:
            next_states = dfa.transitions.get((next(iter(group)), symbol), set())
            next_group = [state for state in partition if next_states.issubset(state)][0]
            dfa_minimized_transitions[(partition.index(group), symbol)] = next_group

    return Automaton(dfa_minimized_states, dfa.alphabet, dfa_minimized_transitions, dfa_minimized_start_state, dfa_minimized_accept_states)

def draw_automaton(automaton, name="automaton"):
    # Dibuja el autómata
    G = nx.DiGraph()

    for state in automaton.states:
        G.add_node(state)

    for transition, next_states in automaton.transitions.items():
        current_state = (transition[0],) if isinstance(transition[0], int) else tuple(transition[0])

        for next_state in next_states:
            next_state_tuple = (next_state,) if isinstance(next_state, int) else tuple(next_state)

            G.add_edge(current_state, next_state_tuple, label=str(transition[1]))

    pos = nx.spring_layout(G)
    labels = {state: str(state) for state in automaton.states}
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=1000, node_color='skyblue')

    # Corrección en la creación de edge_labels
    edge_labels = {}
    for transition, next_states in automaton.transitions.items():
        current_state = (transition[0],) if isinstance(transition[0], int) else tuple(transition[0])

        for next_state in next_states:
            next_state_tuple = (next_state,) if isinstance(next_state, int) else tuple(next_state)

            if current_state in pos and next_state_tuple in pos:
                edge_labels[(current_state, next_state_tuple)] = str(transition[1])

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(f"{name} Automaton")
    plt.show()

def simulate_automaton(automaton, input_string):
    # Simula el autómata con una cadena de entrada y devuelve True si la cadena es aceptada, False en caso contrario
    current_states = epsilon_closure({automaton.start_state}, automaton.transitions)

    for symbol in input_string:
        current_states = move(current_states, symbol, automaton.transitions)
        current_states = epsilon_closure(current_states, automaton.transitions)

    return current_states.intersection(automaton.accept_states) """

def main():
    # Función principal que solicita la expresión regular y la cadena de entrada, y realiza la simulación y minimización de autómatas
    regex = input("Ingrese la expresión regular en notación infix: ")
    input_string = input("Ingrese la cadena a validar: ")

    postfix_expression = shunting_yard(regex)
    #print(f"\nExpresión regular en notación postfix: {' '.join(postfix_expression)}")

    build_tree(postfix_expression)

    """ afn = thompson_algorithm(postfix_expression)
    draw_automaton(afn, name="AFN")

    afd = nfa_to_dfa(afn)
    afd_minimized = minimize_dfa(afd)

    draw_automaton(afd, name="AFD")
    draw_automaton(afd_minimized, name="Minimized AFD")

    afn_result = simulate_automaton(afn, input_string)
    afd_result = simulate_automaton(afd_minimized, input_string) """

    print("\nResultados:")
    """ print(f"Cadena '{input_string}' pertenece al lenguaje definido por la expresión regular (AFN): {bool(afn_result)}")
    print(f"Cadena '{input_string}' pertenece al lenguaje definido por la expresión regular (AFD): {bool(afd_result)}") """

if __name__ == "__main__":
    main()