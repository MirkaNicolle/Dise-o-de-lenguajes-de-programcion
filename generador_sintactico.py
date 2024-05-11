'''Laboratorio E'''

class Grammar:
    def __init__(self):
        self.tokens = []
        self.productions = {}

    def add_token(self, token):
        self.tokens.append(token)

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
                token = line.split()[1]
                grammar.add_token(token)
            elif line == '%%':
                reading_productions = True
            elif reading_productions and line.startswith('rule'):
                current_production = line.split('=')[0].strip().split()[1]
            elif reading_productions and current_production and (line.startswith('|') or line.endswith(';')):
                cleaned_line = line.strip('|').strip(';').strip()
                if cleaned_line:
                    grammar.add_production(current_production, cleaned_line)
            elif line.startswith('/*') or line.startswith('}') or line == '{' or line.startswith('print'):
                continue  

    return grammar

def generate_sintactic_analyzer_code(grammar, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('''# -*- coding: utf-8 -*-
class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        self.children = children if children is not None else []
        self.leaf = leaf

    def __str__(self):
        return f"{self.type}({', '.join(str(child) for child in self.children if child) if self.children else self.leaf})"

class Parser:
    def __init__(self, lexer=None):
        self.lexer = lexer
        self.tokens = []
        self.current_token_index = 0
        self.current_token = None
        if lexer:
            self.tokens = lexer.analyze()  # Suponiendo que analyze() devuelve una lista de tokens
            self.current_token = self.tokens[self.current_token_index] if self.tokens else None

    def set_tokens(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None  # EOF

    def eat(self, token_type):
        if self.current_token and self.current_token['type'] == token_type:
            self.advance()
        else:
            found = self.current_token['type'] if self.current_token else 'EOF'
            raise Exception(f"Expected token type {token_type}, but got {found}")

    def parse_expression(self):
        node = self.parse_term()
        while self.current_token and self.current_token['type'] in ('PLUS', 'MINUS'):
            token_type = self.current_token['type']
            self.advance()
            right_node = self.parse_term()
            if token_type == 'PLUS':
                node = Node('add', children=[node, right_node])
            elif token_type == 'MINUS':
                node = Node('subtract', children=[node, right_node])
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token and self.current_token['type'] in ('MULT', 'DIV'):
            token_type = self.current_token['type']
            self.advance()
            right_node = self.parse_factor()
            if token_type == 'MULT':
                node = Node('multiply', children=[node, right_node])
            elif token_type == 'DIV':
                node = Node('divide', children=[node, right_node])
        return node

    def parse_factor(self):
        if not self.current_token:
            raise Exception("Unexpected end of input while parsing factor")
        if self.current_token['type'] == 'LPAREN':
            self.advance()
            node = self.parse_expression()
            self.eat('RPAREN')
            return node
        elif self.current_token['type'] == 'NUMBER':
            node_value = self.current_token['value']
            self.advance()
            return Node('number', leaf=node_value)
        elif self.current_token['type'] == 'IDENTIFIER':
            node_value = self.current_token['value']
            self.advance()
            return Node('identifier', leaf=node_value)
        else:
            raise Exception(f"Unexpected token {self.current_token['type']}")
''')