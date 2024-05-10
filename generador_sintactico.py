'''Laboratorio E'''

class Grammar:
    def __init__(self):
        self.tokens = []
        self.productions = {}

    def add_token(self, token):
        """Añade un token a la lista de tokens reconocidos por la gramática."""
        self.tokens.append(token)

    def add_production(self, head, rules):
        """Añade una regla de producción a la gramática bajo la cabeza especificada."""
        self.productions[head] = rules

def parse_yapar_file(filepath):
    """Analiza un archivo YAPar y construye un objeto Grammar con los tokens y producciones definidos."""
    grammar = Grammar()
    current_production = None
    reading_productions = False

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('/*') or line == '}' or line.startswith('print') or line == '{':
                continue  # Ignorar líneas que no son relevantes para la gramática
            if line.startswith('%token'):
                token = line.split()[1]
                grammar.add_token(token)
            elif line == '%%':
                reading_productions = True
                continue
            elif reading_productions:
                if line.startswith('rule'):
                    current_production = line.split()[1].strip()  # Asignar nueva cabeza de producción
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

def generate_sintactic_analyzer_code(grammar, output_file):
    code = '''# -*- coding: utf-8 -*-
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def advance(self):
        """Avanza al siguiente token."""
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        """Consume un token del tipo esperado o lanza un error."""
        if self.current_token and self.current_token['type'] == token_type:
            self.advance()
        else:
            found = self.current_token['type'] if self.current_token else 'EOF'
            raise Exception(f"Expected token type {token_type}, but got {found}")

    def parse_expression(self):
        """Analiza una expresión según la gramática definida."""
        node = self.parse_term()
        while self.current_token and self.current_token['type'] in ('PLUS', 'MINUS'):
            token_type = self.current_token['type']
            self.advance()
            right_node = self.parse_term()
            if token_type == 'PLUS':
                node = {"type": "add", "left": node, "right": right_node}
            elif token_type == 'MINUS':
                node = {"type": "subtract", "left": node, "right": right_node}
        return node

    def parse_term(self):
        """Analiza un término, maneja la multiplicación y división."""
        node = self.parse_factor()
        while self.current_token and self.current_token['type'] in ('MULT', 'DIV'):
            token_type = self.current_token['type']
            self.advance()
            right_node = self.parse_factor()
            if token_type == 'MULT':
                node = {"type": "multiply", "left": node, "right": right_node}
            elif token_type == 'DIV':
                node = {"type": "divide", "left": node, "right": right_node}
        return node

    def parse_factor(self):
        """Analiza un factor, que puede ser un número, un identificador, o una expresión entre paréntesis."""
        if not self.current_token:
            raise Exception("Unexpected end of input while parsing factor")
        if self.current_token['type'] == 'LPAREN':
            self.advance()
            node = self.parse_expression()
            self.eat('RPAREN')
            return node
        elif self.current_token['type'] == 'NUMBER':
            value = self.current_token['value']
            self.advance()
            return {"type": "number", "value": value}
        elif self.current_token['type'] == 'IDENTIFIER':
            value = self.current_token['value']
            self.advance()
            return {"type": "identifier", "value": value}
        else:
            raise Exception(f"Unexpected token {self.current_token['type']}")
        '''

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(code)