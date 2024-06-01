from grammar import Grammar

class YaparParser:
    def __init__(self, yapar_file):
        self.yapar_file = yapar_file
        self.productions = []
        self.tokens = set()
        self.non_terminals = set()
        self.start_symbol = None
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
                        self.tokens.add(parts[1])
                elif line == '%%':
                    reading_productions = True
                elif reading_productions:
                    if line.startswith('rule'):
                        current_production = line.split('=')[0].strip().split()[1]
                        if self.start_symbol is None:
                            self.start_symbol = current_production
                    elif line.startswith('|') or line.endswith(';'):
                        cleaned_line = line.strip('|').strip(';').strip()
                        cleaned_line = self.remove_actions(cleaned_line)
                        if cleaned_line:
                            self.productions.append((current_production, cleaned_line.split()))
                            self.non_terminals.add(current_production)
                elif line.startswith('/*') or line == '}' or line == '{' or line.startswith('print'):
                    continue

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
        # Crear el diccionario de producciones
        production_dict = {}
        for head, body in self.productions:
            if head not in production_dict:
                production_dict[head] = []
            production_dict[head].append(body)

        return Grammar(production_dict, self.non_terminals, self.tokens, self.start_symbol)

'''if __name__ == "__main__":
    yapar_parser = YaparParser('hard_yapar.yalp')
    grammar = yapar_parser.get_grammar()
    print("Producciones:", grammar.productions)
    print("Tokens:", grammar.terminals)  # Cambiamos 'tokens' a 'terminals'
    print("No Terminales:", grammar.non_terminals)
    print("Símbolo de Inicio:", grammar.start_symbol)'''