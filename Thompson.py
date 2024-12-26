'''Thompson es un método que convierte una expresión regular en un Autómata Finito No Determinista (AFN)'''

# Thompson.py
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
        self.start_state = start_state
        self.states = [start_state]

def regex_to_afn(postfix_regex):
    stack = []
    i = 0
    while i < len(postfix_regex):
        char = postfix_regex[i]
        if char.isalnum() or char in ('.', '_'):
            start = State()
            end = State(True)
            start.add_transition(char, end)
            stack.append((start, end))
        elif char == '[':
            start = State()
            end = State(True)
            i += 1
            char_class = []
            while postfix_regex[i] != ']':
                if postfix_regex[i] == '\\':
                    i += 1
                char_class.append(postfix_regex[i])
                i += 1
            start.add_transition("".join(char_class), end)
            stack.append((start, end))
            i += 1
        elif char in ['*', '+']:
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

def visualize_afn(afn, token_name, all_graphs):
    dot = graphviz.Digraph(name=f"digraph_afn_{token_name}")
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
    all_graphs.append(dot.source)

def process_yalex_file(input_path, output_path):
    all_graphs = []
    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            if ':=' in line:
                token_name, regex = line.split(':=', 1)
                afn = regex_to_afn(regex.strip())
                if afn:
                    visualize_afn(afn, token_name.strip(), all_graphs)
                else:
                    print(f"Error al generar el AFN para el token: {token_name.strip()}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(all_graphs))

def main(input_path, output_path):
    process_yalex_file(input_path, output_path)