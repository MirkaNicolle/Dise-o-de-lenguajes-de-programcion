'''Laboratorio E'''

from generador_lexico import LexicalAnalyzer
from generador_sintactico import Parser

def read_yalex_file(file_path):
    rules = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reading_rules = False
        for line in file:
            line = line.strip()
            if line.startswith('%token'):
                reading_rules = True
            elif reading_rules and line != '%%':
                if line.startswith('let') or line.startswith('rule'):
                    parts = line.split('=')
                    rule_name = parts[0].strip()
                    rule_pattern = parts[1].strip().replace('{', '').replace('}', '').strip()
                    rules[rule_name] = rule_pattern
                elif line == '%%':
                    reading_rules = False
    return rules

class Grammar:
    def __init__(self):
        self.tokens = {}
        self.productions = {}

    def add_token(self, token, token_type):
        self.tokens[token] = token_type

    def add_production(self, head, production):
        if head not in self.productions:
            self.productions[head] = []
        self.productions[head].append(production)

def parse_yapar_file(filepath):
    grammar = Grammar()
    current_production = None
    reading_productions = False

    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('%token'):
                parts = line.split()
                if len(parts) > 1:
                    grammar.add_token(parts[1], 'TOKEN')
            elif line == '%%':
                reading_productions = True
            elif reading_productions:
                if line.startswith('rule'):
                    current_production = line.split('=')[0].strip().split()[1]
                elif line.startswith('|') or line.endswith(';'):
                    cleaned_line = line.strip('|').strip(';').strip()
                    if cleaned_line:
                        grammar.add_production(current_production, cleaned_line)
            elif line.startswith('/*') or line == '}' or line == '{' or line.startswith('print'):
                continue  
    return grammar

def read_file(file_path):
    """Función para leer el contenido de un archivo de texto."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    yalex_path = 'hard_especificaciones.yalex'
    yapar_path = 'especificaciones_yapar.yalp'

    # Crear analizadores
    lexical_rules = read_yalex_file(yalex_path)
    grammar_rules = parse_yapar_file(yapar_path)

    lexical_analyzer = LexicalAnalyzer(lexical_rules)
    parser = Parser()

    # Ruta del archivo de texto de entrada
    input_file_path = 'hard.txt'  # Asegúrate de que este archivo exista en tu directorio o especifica la ruta completa

    # Leer el archivo de entrada
    input_text = read_file(input_file_path)

    lexical_analyzer.set_input(input_text)
    tokens = []
    print("Generated Tokens:")
    while True:
        token = lexical_analyzer.get_next_token()
        if token is None:
            break
        tokens.append(token)
        print(f"Token: Type={token.type}, Value={token.value}")

    parser.set_tokens(tokens)
    try:
        parser.parse()
        print("Parsing successful.")
    except Exception as e:
        print(f"Parsing failed: {e}")

if __name__ == "__main__":
    main()