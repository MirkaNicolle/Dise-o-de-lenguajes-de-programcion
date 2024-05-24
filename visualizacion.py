import graphviz

def visualize_automaton(automaton):
    dot = graphviz.Digraph(comment='LR(0) Automaton')
    for i, state in enumerate(automaton.states):
        label = "\n".join([f"{head} -> {''.join(body[:dot_pos])}.{''.join(body[dot_pos:])}" for head, body, dot_pos in state])
        dot.node(f"S{i}", label)
    for (from_state, symbol), to_state in automaton.transitions.items():
        dot.edge(f"S{from_state}", f"S{to_state}", label=symbol)
    return dot