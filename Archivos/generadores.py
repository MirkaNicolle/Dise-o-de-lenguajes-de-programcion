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
                    grammar.add_token(parts[1])
            elif line == '%%':
                reading_productions = True
            elif reading_productions:
                if line.startswith('rule'):
                    current_production = line.split('=')[0].strip().split()[1]
                    if grammar.start_symbol is None:
                        grammar.start_symbol = current_production
                elif line.startswith('|') or line.endswith(';'):
                    cleaned_line = line.strip('|').strip(';').strip()
                    if cleaned_line:
                        grammar.add_production(current_production, cleaned_line)
            elif line.startswith('/*') or line == '}' or line == '{' or line.startswith('print'):
                continue  

    grammar.productions[grammar.augmented_start] = [(grammar.start_symbol,)]

    return grammar

def read_file(file_path):
    """Función para leer el contenido de un archivo de texto."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def run_analysis(input_text, yalex_path='easy_especificaciones.yalex', yapar_path='especificaciones_yapar.yalp'):
    lexical_rules = read_yalex_file(yalex_path)
    grammar_rules = parse_yapar_file(yapar_path)

    lexical_analyzer = LexicalAnalyzer(lexical_rules)
    lexical_analyzer.set_input(input_text)
    tokens = []
    output = "Generated Tokens:\n"
    while True:
        token = lexical_analyzer.get_next_token()
        if token is None:
            break
        tokens.append(token)
        output += f"Token: Type={token.type}, Value={token.value}\n"

    parser = Parser(tokens)
    try:
        parse_tree = parser.parse()
        output += "\nSyntactic Analysis:\n"
        output += str(parse_tree) + "\n"
    except Exception as e:
        output += f"Error parsing: {e}\n"
    return output