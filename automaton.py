class LR0Automaton:
    def __init__(self, grammar):
        self.grammar = grammar
        self.states = []
        self.transitions = {}
        self.build_automaton()

    def build_automaton(self):
        start_production = (self.grammar.augmented_start, (self.grammar.start_symbol,), 0)
        self.start_state = self.closure([start_production])
        self.states.append(self.start_state)

        queue = [self.start_state]
        visited = set()
        visited.add(frozenset(self.start_state))

        while queue:
            state = queue.pop(0)
            for symbol in self.grammar.terminals | self.grammar.non_terminals:
                new_state = self.goto(state, symbol)
                if not new_state:
                    continue
                frozenset_new_state = frozenset(new_state)
                if frozenset_new_state not in visited:
                    visited.add(frozenset_new_state)
                    queue.append(new_state)
                    self.states.append(new_state)
                self.transitions[(frozenset(state), symbol)] = frozenset_new_state

    def closure(self, items):
        closure_set = set(items)
        queue = items[:]
        while queue:
            head, body, dot_position = queue.pop(0)
            if dot_position < len(body):
                symbol = body[dot_position]
                if symbol in self.grammar.non_terminals:
                    for production in self.grammar.productions[symbol]:
                        new_item = (symbol, tuple(production), 0)
                        if new_item not in closure_set:
                            closure_set.add(new_item)
                            queue.append(new_item)
        return list(closure_set)

    def goto(self, state, symbol):
        goto_set = []
        for head, body, dot_position in state:
            if dot_position < len(body) and body[dot_position] == symbol:
                new_item = (head, body, dot_position + 1)
                goto_set.append(new_item)
        return self.closure(goto_set) if goto_set else []

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