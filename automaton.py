from grammar import grammar
import graphviz

class LR0Automaton:
    def __init__(self, grammar, common_productions=None):
        self.grammar = grammar
        self.common_productions = common_productions or []
        self.states = []
        self.transitions = {}

    def closure(self, items):
        closure = set(items)
        changed = True
        while changed:
            changed = False
            new_items = set()
            for (head, body, dot_position) in closure:
                if dot_position < len(body) and body[dot_position] in self.grammar.non_terminals:
                    for production in self.grammar.productions[body[dot_position]]:
                        item = (body[dot_position], tuple(production), 0)
                        if item not in closure:
                            new_items.add(item)
                            changed = True
            closure.update(new_items)
        return closure

    def goto(self, items, symbol):
        goto_set = set()
        for (head, body, pos) in items:
            if pos < len(body) and body[pos] == symbol:
                new_item = (head, body, pos + 1)
                goto_set.add(new_item)
        return self.closure(goto_set)

    def build_automaton(self):
        init_items = [(self.grammar.augmented_start, tuple(['.', self.grammar.start_symbol]), 0)]
        for prod in self.common_productions:
            init_items.append((prod[0], tuple(['.', *prod[1]]), 0))

        init_state = self.closure(init_items)

        self.states.append(init_state)
        unmarked_states = [init_state]
        state_index = {tuple(init_state): 0}

        while unmarked_states:
            current_state = unmarked_states.pop(0)
            current_index = state_index[tuple(current_state)]

            for symbol in self.grammar.tokens.union(self.grammar.non_terminals):
                next_state = self.goto(current_state, symbol)
                if next_state and tuple(next_state) not in state_index:
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

common_productions = [('expression', 'PLUS', 'term')]

lr0_automaton = LR0Automaton(grammar, common_productions)
lr0_automaton.build_automaton()
lr0_automaton.visualize()