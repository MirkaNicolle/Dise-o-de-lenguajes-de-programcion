class Grammar:
    def __init__(self):
        self.productions = {}
        self.tokens = set()
        self.non_terminals = set()
        self.first_sets = {}
        self.follow_sets = {}
        self.start_symbol = None
        self.augmented_start = 'S'

    def add_token(self, token):
        self.tokens.add(token)

    def add_production(self, head, production):
        if head not in self.productions:
            self.productions[head] = []
        self.productions[head].append(tuple(production.split()))
        self.non_terminals.add(head)


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
                        # Eliminar el contenido entre llaves manualmente
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

# Ejemplo de uso
if __name__ == "__main__":
    yapar_parser = YaparParser('especificaciones_yapar.yalp')
    grammar = yapar_parser.get_grammar()
    print("Producciones:", grammar.productions)
    print("Tokens:", grammar.tokens)
    print("No Terminales:", grammar.non_terminals)
    print("Símbolo de Inicio:", grammar.start_symbol)