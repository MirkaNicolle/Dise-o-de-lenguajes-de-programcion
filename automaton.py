from grammar import Grammar

class LR0Automaton:
    def __init__(self, grammar):
        self.grammar = grammar
        self.states = []
        self.transitions = {}
        self.start_state = None
        self.build_automaton()

    def closure(self, items):
        closure_set = set(items)
        while True:
            new_items = set()
            for head, body, dot_pos in closure_set:
                if dot_pos < len(body):
                    next_symbol = body[dot_pos]
                    if next_symbol in self.grammar.productions:
                        for production in self.grammar.productions[next_symbol]:
                            new_item = (next_symbol, production, 0)
                            if new_item not in closure_set:
                                new_items.add(new_item)
            if not new_items:
                break
            closure_set.update(new_items)
        return closure_set

    def goto(self, items, symbol):
        goto_set = set()
        for head, body, dot_pos in items:
            if dot_pos < len(body) and body[dot_pos] == symbol:
                new_item = (head, body, dot_pos + 1)
                goto_set.add(new_item)
        return self.closure(goto_set)

    def build_automaton(self):
        start_production = (self.grammar.augmented_start, (self.grammar.start_symbol,), 0)
        self.start_state = self.closure([start_production])
        states = [self.start_state]
        self.states.append(self.start_state)
        unmarked_states = [self.start_state]

        while unmarked_states:
            current_state = unmarked_states.pop()
            symbols = self._get_symbols(current_state)
            for symbol in symbols:
                new_state = self.goto(current_state, symbol)
                if new_state and new_state not in states:
                    states.append(new_state)
                    unmarked_states.append(new_state)
                    self.states.append(new_state)
                self.transitions[(self.states.index(current_state), symbol)] = self.states.index(new_state)

    def _get_symbols(self, items):
        symbols = set()
        for _, body, dot_pos in items:
            if dot_pos < len(body):
                symbols.add(body[dot_pos])
        return symbols