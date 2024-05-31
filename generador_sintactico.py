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
        self.set_tokens(tokens)
        self.parse_tree = None

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
            token = self.current_token
            self.advance()
            return token
        else:
            expected = token_type
            found = self.current_token.type if self.current_token else 'EOF'
            raise Exception(f"Expected token {expected}, but found {found}")

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

    def parse(self):
        stack = [0]
        symbol_stack = []
        while True:
            state = stack[-1]
            action = self.slr_table[state].get(self.current_token.type)
            if action is None:
                raise Exception(f"Syntax error: unexpected token {self.current_token.type}")
            if action.startswith('shift'):
                stack.append(int(action.split()[1]))
                symbol_stack.append(self.current_token)
                self.advance()
            elif action.startswith('reduce'):
                production = self.grammar.productions[int(action.split()[1])]
                head, body = production[0], production[1]
                for _ in body:
                    stack.pop()
                    symbol_stack.pop()
                stack.append(self.slr_table[stack[-1]].get(head))
                symbol_stack.append(head)
            elif action == 'Accept':
                return True
            else:
                raise Exception(f"Invalid action: {action}")