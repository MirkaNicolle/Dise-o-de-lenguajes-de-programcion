from grammar import grammar
import graphviz

class LR0Automaton:
    def __init__(self, grammar):
        self.grammar = grammar
        self.states = []  # States in the automaton
        self.transitions = {}  # Transitions between states

    def closure(self, items):
        closure = set(items)  # Asegúrate de que items ya sean tuplas
        changed = True
        while changed:
            changed = False
            new_items = set()
            for (head, body, dot_position) in closure:
                if dot_position < len(body) and body[dot_position] in self.grammar.non_terminals:
                    for production in self.grammar.productions[body[dot_position]]:
                        # Convertir body y production a tuplas si no lo son
                        item = (body[dot_position], tuple(production), 0)
                        if item not in closure:
                            new_items.add(item)
                            changed = True
            closure.update(new_items)
        return closure

    def goto(self, items, symbol):
        goto_set = set()
        for (head, body, dot_position) in items:
            if dot_position < len(body) and body[dot_position] == symbol:
                goto_set.add((head, body, dot_position + 1))
        return self.closure(goto_set)

    def build_automaton(self):
        init_item = (self.grammar.augmented_start, tuple(['.', self.grammar.start_symbol]), 0)
        init_state = self.closure([init_item])

        self.states.append(init_state)
        unmarked_states = [init_state]
        state_index = {tuple(init_state): 0}

        while unmarked_states:
            current_state = unmarked_states.pop(0)
            current_index = state_index[tuple(current_state)]

            for symbol in self.grammar.tokens.union(self.grammar.non_terminals):
                next_state = self.goto(current_state, symbol)
                if next_state and next_state not in self.states:
                    state_index[tuple(next_state)] = len(self.states)
                    self.states.append(next_state)
                    unmarked_states.append(next_state)
                    self.transitions[(current_index, symbol)] = state_index[tuple(next_state)]

    def visualize(self):
        dot = graphviz.Digraph(comment='LR(0) Automaton')

        for i, state in enumerate(self.states):
            label = "\n".join([
                f"{item[0]} -> {' '.join(item[1][:item[2]] + ('*',) + item[1][item[2]:])}"
                for item in state
            ])
            dot.node(str(i), label=label)

        for (from_state, symbol), to_state in self.transitions.items():
            dot.edge(str(from_state), str(to_state), label=symbol)

        dot.render('lr0_automaton', view=True)

# Example usage
lr0_automaton = LR0Automaton(grammar)
lr0_automaton.build_automaton()
lr0_automaton.visualize()