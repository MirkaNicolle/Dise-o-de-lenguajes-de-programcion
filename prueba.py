class Grammar:
    def __init__(self):
        self.tokens = []
        self.productions = {}

    def add_token(self, token):
        self.tokens.append(token)

    def add_production(self, head, rules):
        self.productions[head] = rules

def parse_yapar_file(filepath):
    grammar = Grammar()
    current_production = None
    reading_productions = False

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('/*') or line == '}' or line.startswith('print') or line == '{':
                continue  # Ignorar líneas vacías, comentarios, cierres de bloques y prints
            if line.startswith('%token'):
                token = line.split()[1]
                grammar.add_token(token)
            elif line == '%%':
                reading_productions = True
                continue
            elif reading_productions:
                if line.startswith('rule'):
                    current_production = line.split()[1].strip()  # Iniciar una nueva producción
                    grammar.add_production(current_production, [])
                elif current_production and (line.startswith('|') or line.endswith(';')):
                    rules = line.split('|')
                    for rule in rules:
                        rule_clean = rule.strip().strip(';')
                        if rule_clean:
                            grammar.productions[current_production].append(rule_clean)
                elif current_production and line:
                    if line.startswith('{'):
                        continue  # Ignorar apertura de bloques
                    grammar.productions[current_production].append(line.strip())

    return grammar

def main():
    file_path = 'example.yalp'  # Asegúrate de que la ruta del archivo es correcta
    grammar = parse_yapar_file(file_path)
    tokens = grammar.tokens
    productions = grammar.productions
    print("Tokens:", tokens)
    print("Productions:", productions)

if __name__ == '__main__':
    main()
