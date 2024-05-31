class Grammar:
    def __init__(self):
        self.productions = {}
        self.tokens = set()
        self.non_terminals = set()
        self.first_sets = {}
        self.follow_sets = {}
        self.start_symbol = None
        self.augmented_start = 'S'
        self.production_list = []

    def add_token(self, token):
        self.tokens.add(token)

    def add_production(self, head, production):
        if head not in self.productions:
            self.productions[head] = []
        self.productions[head].append(tuple(production.split()))
        self.production_list.append((head, tuple(production.split())))
        self.non_terminals.add(head)
        if head not in self.first_sets:
            self.first_sets[head] = set()
        if head not in self.follow_sets:
            self.follow_sets[head] = set()

    def get_production(self, index):
        return self.production_list[index]

    def get_productions(self):
        return self.production_list

    def primero_sets(self):
        changed = True
        while changed:
            changed = False
            for head, productions in self.productions.items():
                for production in productions:
                    for symbol in production:
                        if symbol in self.tokens:
                            if symbol not in self.first_sets[head]:
                                self.first_sets[head].add(symbol)
                                changed = True
                            break
                        elif symbol in self.non_terminals:
                            before_change = len(self.first_sets[head])
                            self.first_sets[head].update(self.first_sets[symbol] - {None})
                            if None in self.first_sets[symbol]:
                                continue
                            if len(self.first_sets[head]) > before_change:
                                changed = True
                            break
                        if symbol == production[-1]:
                            self.first_sets[head].add(None)

    def siguiente_sets(self):
        for non_terminal in self.non_terminals:
            self.follow_sets[non_terminal] = set()
        if self.start_symbol:
            self.follow_sets[self.start_symbol].add('$')

        changed = True
        while changed:
            changed = False
            for head, productions in self.productions.items():
                for production in productions:
                    follow_temp = self.follow_sets[head].copy()

                    for i in reversed(range(len(production))):
                        symbol = production[i]
                        if symbol in self.non_terminals:
                            before_change = len(self.follow_sets[symbol])
                            self.follow_sets[symbol].update(follow_temp)
                            if None in self.first_sets[symbol]:
                                follow_temp.update(self.first_sets[symbol] - {None})
                            else:
                                follow_temp = self.first_sets[symbol]
                            if len(self.follow_sets[symbol]) > before_change:
                                changed = True
                        else:
                            follow_temp = self.first_sets[symbol] if symbol in self.first_sets else set()

class YaparParser:
    def __init__(self, yapar_file):
        self.yapar_file = yapar_file
        self.grammar = Grammar()
        self.parse_yapar_file()

    def parse_yapar_file(self):
        current_production = None
        reading_productions = False

        with open(self.yapar_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('%token'):
                    parts = line.split()
                    if len(parts) > 1:
                        self.grammar.add_token(parts[1])
                elif line == '%%':
                    reading_productions = True
                elif reading_productions:
                    if line.startswith('rule'):
                        current_production = line.split('=')[0].strip().split()[1]
                        if self.grammar.start_symbol is None:
                            self.grammar.start_symbol = current_production
                    elif line.startswith('|') or line.endswith(';'):
                        cleaned_line = line.strip('|').strip(';').strip()
                        cleaned_line = self.remove_actions(cleaned_line)
                        if cleaned_line:
                            self.grammar.add_production(current_production, cleaned_line)
                elif line.startswith('/*') or line == '}' or line == '{' or line.startswith('print'):
                    continue

        self.grammar.productions[self.grammar.augmented_start] = [(self.grammar.start_symbol,)]

    def remove_actions(self, line):
        cleaned_line = ''
        inside_action = False
        for char in line:
            if char == '{':
                inside_action = True
            elif char == '}':
                inside_action = False
                continue
            if not inside_action:
                cleaned_line += char
        return cleaned_line.strip()

    def get_grammar(self):
        return self.grammar

'''if __name__ == "__main__":
    yapar_parser = YaparParser('hard_yapar.yalp')
    grammar = yapar_parser.get_grammar()
    print("Producciones:", grammar.productions)
    print("Tokens:", grammar.tokens)
    print("No Terminales:", grammar.non_terminals)
    print("Símbolo de Inicio:", grammar.start_symbol)'''