from automaton import LR0Automaton

class SLRTable:
    def __init__(self, grammar):
        self.grammar = grammar
        self.automaton = LR0Automaton(grammar)  # Asegúrate de tener esta clase implementada
        self.slr_table = self.construct_slr_table()

    def construct_slr_table(self):
        slr_table = {}
        follow_sets = self.grammar.follow_sets

        for state in self.automaton.states:
            state_key = tuple(state)  # Convierte el estado a una tupla para que sea hashable
            slr_table[state_key] = {}
            for item in state.items:
                if item.is_final():
                    if item.production.head == self.grammar.augmented_start:
                        slr_table[state_key]['$'] = 'accept'
                    else:
                        for terminal in follow_sets[item.production.head]:
                            slr_table[state_key][terminal] = f'reduce {item.production}'
                else:
                    next_symbol = item.next_symbol()
                    if next_symbol in self.grammar.tokens:
                        next_state = self.automaton.go_to(state, next_symbol)
                        next_state_key = tuple(next_state)  # Convierte el siguiente estado a una tupla para que sea hashable
                        slr_table[state_key][next_symbol] = f'shift {next_state_key}'
                    elif next_symbol in self.grammar.non_terminals:
                        next_state = self.automaton.go_to(state, next_symbol)
                        next_state_key = tuple(next_state)  # Convierte el siguiente estado a una tupla para que sea hashable
                        slr_table[state_key][next_symbol] = next_state_key
        return slr_table

    def display_slr_table(self):
        for state, actions in self.slr_table.items():
            print(f"Estado {state}:")
            for symbol, action in actions.items():
                print(f"  {symbol}: {action}")
        return self.slr_table