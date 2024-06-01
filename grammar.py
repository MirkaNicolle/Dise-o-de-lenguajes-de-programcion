class Grammar:
    def __init__(self, productions, non_terminals, terminals, start_symbol):
        self.productions = productions
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.augmented_start = f"{start_symbol}'"
        self.productions[self.augmented_start] = [[start_symbol]]
        self.first_sets = {nt: set() for nt in non_terminals}
        self.follow_sets = {nt: set() for nt in non_terminals}
        self.follow_sets[self.augmented_start] = set()

    def calculate_first_sets(self):
        for terminal in self.terminals:
            self.first_sets[terminal] = {terminal}

        def first(symbol, visited):
            if symbol in self.first_sets and self.first_sets[symbol]:
                return self.first_sets[symbol]
            if symbol in visited:
                return set()  # Return empty set to avoid infinite recursion
            visited.add(symbol)
            first_set = set()
            for head, bodies in self.productions.items():
                for body in bodies:
                    if head == symbol:
                        if not body:
                            first_set.add('')
                        else:
                            for production_symbol in body:
                                if production_symbol not in self.first_sets:
                                    self.first_sets[production_symbol] = set()
                                production_first_set = first(production_symbol, visited)
                                first_set.update(production_first_set - {''})
                                if '' not in production_first_set:
                                    break
                            else:
                                first_set.add('')
            self.first_sets[symbol] = first_set
            visited.remove(symbol)
            return first_set

        for non_terminal in self.non_terminals:
            first(non_terminal, set())

    def calculate_follow_sets(self):
        self.follow_sets[self.start_symbol].add('$')

        def follow(symbol):
            follow_set = self.follow_sets[symbol]
            for head, bodies in self.productions.items():
                for body in bodies:
                    for i, production_symbol in enumerate(body):
                        if production_symbol == symbol:
                            next_symbols = body[i + 1:]
                            if next_symbols:
                                next_first_set = self.first(next_symbols)
                                follow_set.update(next_first_set - {''})
                                if '' in next_first_set:
                                    follow_set.update(self.follow_sets.get(head, set()))
                            else:
                                follow_set.update(self.follow_sets.get(head, set()))
            return follow_set

        for non_terminal in self.non_terminals:
            follow(non_terminal)
        follow(self.augmented_start)

    def first(self, symbols):
        first_set = set()
        for symbol in symbols:
            symbol_first_set = self.first_sets.get(symbol, set())
            first_set.update(symbol_first_set - {''})
            if '' not in symbol_first_set:
                break
        else:
            first_set.add('')
        return first_set