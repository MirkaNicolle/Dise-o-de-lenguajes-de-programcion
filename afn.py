'''
Construccion de un AFN a partir de una expresion regular r 
'''
import graphviz

'''
Estados para el AFN
'''
class State:
    id_counter = 0

    def __init__(self):
        self.transitions = {}
        self.id = State.id_counter
        State.id_counter += 1
        self.final = False
    
    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]

'''
Construccion de un AFN 
'''
def build_nfa(postfix_expr):
    stack = []

    for symbol in postfix_expr:
        if symbol == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State()
            end = State()
            start.add_transition('ε', nfa1)
            start.add_transition('ε', nfa2)
            nfa1.final = False
            nfa2.final = False
            nfa1.add_transition('ε', end)
            nfa2.add_transition('ε', end)
            stack.append(start)
        elif symbol == '.':
            state = State()
            state.add_transition('.', State())
            stack.append(state)
        elif symbol == ';':
            state = State()
            state.add_transition(';', State())
            stack.append(state)
        elif symbol == '*':
            nfa1 = stack.pop()
            start = State()
            end = State()
            start.add_transition('ε', nfa1)
            start.add_transition('ε', end)
            nfa1.final = False
            nfa1.add_transition('ε', nfa1)
            nfa1.add_transition('ε', end)
            stack.append(start)
        else:
            state = State()
            state.add_transition(symbol, State())
            stack.append(state)

    nfa = stack.pop()
    nfa.final = True
    return nfa

'''
Leer el archivo con la expresion postfix
'''
def read_postfix_expr(file_path):
    with open(file_path, 'r') as file:
        postfix_expr = file.read().strip()

    return postfix_expr

'''
Funcion para vizualizar el AFN
'''
def visualize_nfa(nfa):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')
    dot.attr('node', shape='circle')
    dot.node(str(nfa.id))

    stack = [nfa]
    visited = set()

    while stack:
        state = stack.pop()

        if state.id in visited:
            continue
        visited.add(state.id)

        if state.final:
            dot.attr('node', shape='doublecircle')
            dot.node(str(state.id))
        else:
            dot.attr('node', shape='circle')
            dot.node(str(state.id))

        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                dot.edge(str(state.id), str(next_state.id), label=symbol)

                if next_state.id not in visited:
                    stack.append(next_state)

    return dot

'''
Obtencion de estados
'''
def get_states(state):
    states = set([state])
    queue = [state]

    while queue:
        state = queue.pop(0)

        for state2 in state.epsilon_transitions:
            if state2 not in states:
                states.add(state2)
                queue.append(state2)

    return states

'''
Definicion de variables 
'''
def postfix_to_nfa_and_visualize(postfix):
    nfa = build_nfa(postfix)
    dot = visualize_nfa(nfa)
    dot.render('nfa', view=True)

with open('postfix.txt', 'r') as file:
    postfix = file.readline()

postfix_to_nfa_and_visualize(postfix)