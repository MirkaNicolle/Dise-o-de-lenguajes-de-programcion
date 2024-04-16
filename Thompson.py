'''Thompson es un método que convierte una expresión regular en un Autómata Finito No Determinista (AFN)'''

import graphviz

'''representa un estado dentro de un afn. cada estado puede tener multiples transiciones a otros estados'''
class State:
    def __init__(self, accept=False):
        self.accept = accept  #muestra si el estado es de aceptacion
        self.transitions = {}  #diccionario para transiciones: clave = simbolo, valor = lista de estados destintos

    '''añade una transicion desde este estado a otro estado segun un simbolo'''
    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)  #si el simbolo ya existe en el diccionario, agrega el estado a la lista
        else:
            self.transitions[symbol] = [state]  #si el simbolo no existe, crea una nueva entrada en el diccionario

'''representacion un automata finito no determinista (afn)'''
class AFN:
    def __init__(self, start_state):
        self.start_state = start_state  #estado inicial del afn
        self.states = [start_state]  #lista de estados que comienza con el estado inicial

    def add_state(self, state):
        self.states.append(state)  #añade un nuevo estado a la lista de estados

'''conversion postfix a un afn utilizando mcnaughton-yamada-thompson'''
def regex_to_afn(postfix_regex):
    stack = []  #pila para construir subcomponentes del afn
    state_id = 1  #iniciar los ids de estado desde 1

    for char in postfix_regex:
        if char.isalnum():  #simbolo
            start = State()
            end = State(True)
            start.add_transition(char, end)  #crea una transicion entre un estado inicial y un estado de aceptacion
            stack.append((start, end))  #empuja la pareja de estados al stack
        elif char == '|':  #union
            afn2 = stack.pop()
            afn1 = stack.pop()
            start = State()
            end = State(True)
            start.add_transition(None, afn1[0])
            start.add_transition(None, afn2[0])  #crea transiciones epsilon desde el nuevo estado inicial a los estados iniciales de afn1 y afn2
            afn1[1].accept = False
            afn2[1].accept = False
            afn1[1].add_transition(None, end)
            afn2[1].add_transition(None, end)  #desactiva la aceptacion en los estados finales de afn1 y afn2 y los conecta al nuevo estado final
            stack.append((start, end))
        elif char == '.' or char == '•':  #concatenacion
            afn2 = stack.pop()
            afn1 = stack.pop()
            afn1[1].accept = False
            afn1[1].add_transition(None, afn2[0])  #conecta el estado final de afn1 al estado inicial de afn2
            stack.append((afn1[0], afn2[1]))  #el resultado es un afn que va desde el estado inicial de afn1 al estado final de afn2
        elif char == '*':  #cierre de kleene
            afn = stack.pop()
            start = State()
            end = State(True)
            start.add_transition(None, afn[0])
            start.add_transition(None, end)  #el nuevo estado inicial tiene transiciones epsilon a el estado inicial del sub-afn y al nuevo estado final
            afn[1].accept = False
            afn[1].add_transition(None, afn[0])
            afn[1].add_transition(None, end)  #el estado final del sub-afn se conecta de nuevo a su estado inicial y al estado final
            stack.append((start, end))

    if stack:
        afn = stack.pop()
        return AFN(afn[0])  #afn construido
    return None

def visualize_afn(afn):
    dot = graphviz.Digraph(format='png')
    seen = set()
    state_names = {}

    def visualize(state):
        if state in seen:
            return
        seen.add(state)
        state_name = 'S' + str(len(seen)) #nombre secuencial simple para cada estado antes de procesar las transiciones
        state_names[state] = state_name
        if state.accept:
            dot.node(state_name, shape='doublecircle')
        else:
            dot.node(state_name)
        for symbol, states in state.transitions.items():
            for s in states:
                if s not in seen: #comprobacion del estado destino tambien sea procesado y añadido a state_names
                    visualize(s)
                label = symbol if symbol is not None else 'ε'
                dot.edge(state_name, state_names[s], label=label)

    visualize(afn.start_state)
    dot.render('Thompson AFN', view=True)

def main():
    with open('postfix.txt', 'r') as file:
        postfix_regex = file.read().strip()
    afn = regex_to_afn(postfix_regex)
    if afn:
        visualize_afn(afn)
    else:
        print("error al generar el afn.")

if __name__ == '__main__':
    main()