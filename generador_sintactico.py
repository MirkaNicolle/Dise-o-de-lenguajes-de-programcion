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

    def __repr__(self):
        return f"Token('{self.type}', '{self.value}')"

class Parser:
    def __init__(self, grammar, slr_table, tokens=None):
        self.grammar = grammar
        self.slr_table = slr_table
        self.actions_log = []  # Registro de acciones
        self.set_tokens(tokens if tokens is not None else [])  # Asegurarse de que tokens sea una lista

    def set_tokens(self, tokens):
        self.tokens = [Token(token.type, token.value) for token in tokens]
        self.current_index = 0
        self.current_token = self.tokens[self.current_index] if self.tokens else None

    def advance(self):
        self.current_index += 1
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
        else:
            self.current_token = None

    def parse(self):
        stack = [0]
        symbol_stack = []
        self.actions_log.append("Parsing started.")

        while True:
            state = stack[-1]
            action = self.slr_table.get(state, {}).get(self.current_token.type)
            if action is None:
                self.actions_log.append(f"Syntax error: unexpected token {self.current_token.type}")
                return False
            if action.startswith('shift'):
                next_state = int(action.split()[1])
                stack.append(next_state)
                symbol_stack.append(self.current_token)
                self.actions_log.append(f"Shift to state {next_state} with token {self.current_token}")
                self.advance()
            elif action.startswith('reduce'):
                production_number = int(action.split()[1])
                head, body = self.grammar.productions[production_number]
                for _ in body:
                    stack.pop()
                    symbol_stack.pop()
                next_state = self.slr_table[stack[-1]].get(head)
                stack.append(next_state)
                symbol_stack.append(Token(head, None))
                self.actions_log.append(f"Reduce using production {head} -> {body}")
            elif action == 'Accept':
                self.actions_log.append("Parsing completed successfully.")
                return True
            else:
                self.actions_log.append(f"Invalid action: {action}")
                return False

    def parse_expression(self):
        node = self.parse_term()
        while self.current_token and self.current_token.type in ['PLUS', 'MINUS']:
            operator = self.current_token.type
            self.eat(operator)
            right = self.parse_term()
            node = Node(operator, [node, right])
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token and self.current_token.type in ['MULT', 'DIV']:
            operator = self.current_token.type
            self.eat(operator)
            right = self.parse_factor()
            node = Node(operator, [node, right])
        return node

    def parse_factor(self):
        if self.current_token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_expression()
            self.eat('RPAREN')
            return node
        elif self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.eat('NUMBER')
            return Node('number', [], value)
        elif self.current_token.type == 'IDENTIFIER':
            value = self.current_token.value
            self.eat('IDENTIFIER')
            return Node('identifier', [], value)