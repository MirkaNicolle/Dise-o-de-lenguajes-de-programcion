'''
Laboratorio AB
Lenguajes de programación   
9 de febrero de 2024

Mirka Monzón 18139
Main
'''
import networkx as nx
import matplotlib.pyplot as plt

class State:
    def __init__(self, label, is_accepting=False):
        self.label = label
        self.is_accepting = is_accepting
        self.transitions = {}

def infix_to_postfix(infix_expression):
    precedence = {'*': 3, '.': 2, '|': 1, '(': 0}
    output = []
    stack = []

    for symbol in infix_expression:
        if symbol.isalnum():
            output.append(symbol)
        elif symbol == '(':
            stack.append(symbol)
        elif symbol == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and precedence[stack[-1]] >= precedence[symbol]:
                output.append(stack.pop())
            stack.append(symbol)

    while stack:
        output.append(stack.pop())

    return ''.join(output)

def thompson_construction(postfix_expression):
    stack = []

    for symbol in postfix_expression:
        if symbol.isalnum():
            new_state = State(symbol)
            stack.append(new_state)
        else:
            if symbol == '*':
                state = stack.pop()
                new_state = State('ε', is_accepting=True)
                state.transitions[new_state] = 'ε'
                new_state.transitions[state] = 'ε'
                stack.append(new_state)
            elif symbol == '|':
                state2 = stack.pop()
                state1 = stack.pop()
                new_state = State('ε', is_accepting=True)
                new_state.transitions[state1] = 'ε'
                new_state.transitions[state2] = 'ε'
                stack.append(new_state)
            elif symbol == '.':
                state2 = stack.pop()
                state1 = stack.pop()
                state1.is_accepting = False
                state1.transitions[state2] = 'ε'
                stack.append(state1)

    return stack.pop()

def nfa_to_dfa(nfa):
    return nfa
    # Implementa la construcción de subconjuntos (Subset Construction) aquí
    # Devuelve el AFD resultante

def minimize_dfa(dfa):
    return dfa
    # Implementa el algoritmo de minimización para reducir el número de estados en el AFD
    # Devuelve el AFD minimizado

def visualize_graph(states, filename='graph'):
    G = nx.DiGraph()

    for state in states:
        G.add_node(state.label, shape='circle', color='black', peripheries=2 if state.is_accepting else 1)

        for next_state, symbol in state.transitions.items():
            G.add_edge(state.label, next_state.label, label=symbol)

    pos = nx.spring_layout(G)

    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1000, node_color='lightblue', font_color='black', font_size=10, arrowsize=20, connectionstyle='arc3,rad=0.1')

    plt.savefig(f'{filename}.png', format='png')
    plt.show()

def simulate_dfa(dfa, input_string):
    return dfa
    # Implementa la simulación de un AFD aquí
    # Devuelve True si la cadena es aceptada, False en caso contrario

# Ejemplo de uso
infix_expression = "(a|b)*abb"
postfix_expression = infix_to_postfix(infix_expression)

nfa = thompson_construction(postfix_expression)
visualize_graph([nfa], filename='nfa_graph')

dfa = nfa_to_dfa(nfa)
visualize_graph([dfa], filename='dfa_graph')

minimized_dfa = minimize_dfa(dfa)
visualize_graph([minimized_dfa], filename='minimized_dfa_graph')

input_string = "abb"
if simulate_dfa(minimized_dfa, input_string):
    print(f"{input_string} pertenece al lenguaje generado por la expresión regular.")
else:
    print(f"{input_string} no pertenece al lenguaje generado por la expresión regular.")