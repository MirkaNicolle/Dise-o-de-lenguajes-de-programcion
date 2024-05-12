'''Laboratorio E'''

# -*- coding: utf-8 -*-
class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        self.children = children if children is not None else []
        self.leaf = leaf

    def __str__(self):
        return f"{self.type}({', '.join(str(child) for child in self.children if child) if self.children else self.leaf})"

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

class Parser:
    def __init__(self, tokens=None):
        self.set_tokens(tokens)

    def set_tokens(self, tokens):
        self.tokens = tokens
        self.current_index = 0
        self.current_token = self.tokens[self.current_index] if self.tokens else None

    def advance(self):
        self.current_index += 1
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
        else:
            self.current_token = None

    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.advance()
        else:
            raise Exception(f"Expected {token_type}, found {self.current_token.type if self.current_token else 'EOF'}")

    def parse_expression(self):
        if self.current_token and self.current_token.type in ['PLUS', 'MINUS']:
            left = self.parse_term()
            while self.current_token and self.current_token.type in ['PLUS', 'MINUS']:
                operator = self.current_token.type
                self.eat(operator)
                right = self.parse_term()
                left = Node(operator, [left, right])
        else:
            left = self.parse_term()
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token and self.current_token.type in ['MULT', 'DIV']:
            operator = self.current_token.type
            self.eat(operator)
            right = self.parse_factor()
            left = Node(operator, [left, right])
        return left

    def parse_factor(self):
        if self.current_token.type == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expression()
            self.eat('RPAREN')
            return expr
        elif self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.eat('NUMBER')
            return Node('number', [], value)
        elif self.current_token.type == 'IDENTIFIER':
            value = self.current_token.value
            self.eat('IDENTIFIER')
            return Node('identifier', [], value)
        
    def parse(self):
        print("Parsing has started.")  # Mensaje simple para confirmar que el método funciona.
        # Implementar la lógica de parsing aquí, actualmente solo imprime los tokens recibidos.
        '''for token in self.tokens:
            print(f"Token: {token.type}, Value: {token.value}")'''