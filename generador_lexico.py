'''Laboratorio D'''

# -*- coding: utf-8 -*-
from ShuntingYard import to_postfix
from Thompson import regex_to_afn
from Subconjuntos import afn_to_afd
from Minimizacion import minimize_afd

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):  
        return f"Token('{self.type}', '{self.value}')"

class LexicalAnalyzer:
    def __init__(self, input_text=None):
        self.input = input_text
        self.current_position = 0
        self.total_length = len(input_text) if input_text else 0

    def process_regex_to_afd(self, regex):  
        postfix = to_postfix(regex)  
        afn = regex_to_afn(postfix) 
        afd = afn_to_afd(afn) 
        minimized_afd = minimize_afd(afd)  
        return minimized_afd

    def afd_to_dict(self, afd):  
        state_dict = {}
        for state in afd.states:
            state_id = id(state)
            state_dict[state_id] = {'accept': state.accept, 'transitions': {}}
            for symbol, states in state.transitions.items():
                state_dict[state_id]['transitions'][symbol] = [id(s) for s in states]
        start_state_id = id(afd.start_state)
        return start_state_id, state_dict

    def set_input(self, input_text):
        self.input = input_text
        self.current_position = 0
        self.total_length = len(input_text)

    def get_next_token(self):
        while self.current_position < self.total_length:
            current_char = self.input[self.current_position]

            if current_char.isspace():
                self.current_position += 1
                continue

            if current_char == '/':
                if self.current_position + 1 < self.total_length and self.input[self.current_position + 1] == '/':
                    self.skip_single_line_comment()
                    continue
                elif self.current_position + 1 < self.total_length and self.input[self.current_position + 1] == '*':
                    self.skip_multi_line_comment()
                    continue

            if current_char.isdigit() or (current_char == '.' and self.current_position + 1 < self.total_length and self.input[self.current_position + 1].isdigit()):
                return self.get_number()

            if current_char.isalpha() or current_char == '_':
                return self.get_identifier()

            if current_char in "+-*/()=.,;:{}[]<>!&|%^'@":
                return self.get_operator()

            self.current_position += 1

        return None

    def analyze(self, text):
        self.set_input(text)  
        results = []
        errors = []
        while self.current_position < self.total_length:
            if self.input[self.current_position] == '"' and (self.current_position + 1 < self.total_length and self.input[self.current_position + 1] != "\\\\"):
                result, new_position = self.handle_string(self.input, self.current_position)
                if result is not None:
                    results.append(Token("String", result))
                self.current_position = new_position
            elif self.input[self.current_position].isdigit():
                result, new_position = self.handle_number(self.input, self.current_position)
                results.append(Token("Number", result))
                self.current_position = new_position
            elif self.input[self.current_position].isalpha() or self.input[self.current_position] == '_':
                result, new_position = self.handle_identifier(self.input, self.current_position)
                results.append(Token("Identifier", result))
                self.current_position = new_position
            elif self.input[self.current_position].isspace():
                self.current_position = self.handle_whitespace(self.input, self.current_position)
            elif self.input[self.current_position] in "+-*/()=.,;:{}[]<>!&|%^'@":
                result, new_position = self.handle_operator(self.input, self.current_position)
                results.append(Token("Operator", result))
                self.current_position = new_position
            elif self.input[self.current_position] == '/' and self.current_position + 1 < self.total_length and self.input[self.current_position + 1] == '/':
                self.current_position = self.handle_single_line_comment(self.input, self.current_position + 2)
            elif self.input[self.current_position] == '/' and self.current_position + 1 < self.total_length and self.input[self.current_position + 1] == '*':
                self.current_position = self.handle_multi_line_comment(self.input, self.current_position + 2)
            else:
                errors.append(f"Unknown character: {self.input[self.current_position]} at position {self.current_position}")
                self.current_position += 1
        if errors:
            results.append(Token("Error", " ".join(errors)))
        '''for token in results:
            print(f"Token created: Type={token.type}, Value={token.value}") 
        return results'''
    
    def skip_whitespace(self):
        while self.current_position < self.total_length and self.input[self.current_position].isspace():
            self.current_position += 1
    
    def handle_string(self, text, i):
        if text[i] == '"' and (i == 0 or text[i-1] != '\\\\'):  
            i += 1
            start = i
            while i < len(text):
                if text[i] == '"' and text[i-1] != '\\\\':  
                    return text[start:i], i + 1
                i += 1
            return text[start:], i
        return None, i
    
    def get_number(self):
        start_position = self.current_position
        while self.current_position < self.total_length and (self.input[self.current_position].isdigit() or self.input[self.current_position] == '.'):
            self.current_position += 1

        value = self.input[start_position:self.current_position]
        return Token('FLOAT' if '.' in value else 'NUMBER', value)

    def get_identifier(self):
        start_position = self.current_position
        while self.current_position < self.total_length and (self.input[self.current_position].isalpha() or self.input[self.current_position] == '_'):
            self.current_position += 1

        value = self.input[start_position:self.current_position].upper()
        return Token('IDENTIFIER', value)

    def handle_number(self, text, i):
        num = ""
        while i < len(text) and text[i].isdigit():
            num += text[i]
            i += 1
        return int(num), i

    def handle_identifier(self, text, i):
        ident = ""
        while i < len(text) and (text[i].isalpha() or text[i] == '_'):
            ident += text[i]
            i += 1
        return ident.upper(), i

    def handle_whitespace(self, text, i):
        while i < len(text) and text[i].isspace():
            i += 1
        return i

    def get_operator(self):
        operator = self.input[self.current_position]
        self.current_position += 1
        return Token('OPERATOR', operator)

    def handle_single_line_comment(self, text, i):
        while i < len(text) and text[i] != ' ':
            i += 1
        return i

    def handle_multi_line_comment(self):
        self.current_position += 2  
        while self.current_position + 1 < self.total_length:
            if self.input[self.current_position] == '*' and self.input[self.current_position + 1] == '/':
                self.current_position += 2  
                return
            self.current_position += 1
        raise Exception("End of file reached without closing multi-line comment") 

    def skip_single_line_comment(self):
        while self.current_position < self.total_length and self.input[self.current_position] != '\\n':
            self.current_position += 1
        self.current_position += 1

    def skip_multi_line_comment(self):
        self.current_position += 2
        while self.current_position + 1 < self.total_length:
            if self.input[self.current_position] == '*' and self.input[self.current_position + 1] == '/':
                self.current_position += 2
                return
            self.current_position += 1
    
    def handle_operator(self, text, i):
        start = i
        while i < len(text) and text[i] in "+-*/()=.,;:{}[]<>!&|%^'@":
            i += 1
        operator = text[start:i]
        return operator, i