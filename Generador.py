'''Laboratorio D'''

# -*- coding: utf-8 -*-
from ShuntingYard import to_postfix
from Thompson import regex_to_afn
from Subconjuntos import afn_to_afd
from Minimizacion import minimize_afd

def read_yalex_file(file_path):
    tokens = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        '''for line in file:
            if ':=' in line:
                token_name, regex = line.split(':=')
                tokens[token_name.strip()] = regex.strip()  '''
    return tokens 

def process_regex_to_afd(regex):
    postfix = to_postfix(regex) #conversion de expresion regular en notacion postfix
    afn = regex_to_afn(postfix) #generacion de AFN
    afd = afn_to_afd(afn) # AFN A AFD
    minimized_afd = minimize_afd(afd) #minimizacion de AFD
    return minimized_afd 

def afd_to_dict(afd):
    state_dict = {}
    for state in afd.states: #creacion de un diccionario para representar los estados y transiciones del AFD
        state_id = id(state)
        state_dict[state_id] = {'accept': state.accept, 'transitions': {}}
        for symbol, states in state.transitions.items(): #almacena las transiciones por cada simbolo a los estados correspondientes
            state_dict[state_id]['transitions'][symbol] = [id(s) for s in states]
    start_state_id = id(afd.start_state)
    return start_state_id, state_dict  # devuelve el id del estado inicial y el diccionario de estados

def generate_lexical_analyzer_code(tokens, output_file): #codigo fuente para analizador lexico
    code = '''
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return f"{self.type}: {self.value}"

class LexicalAnalyzer:
    def __init__(self, afds=None, state_dicts=None):
        if afds is None:
            afds = {}  
        if state_dicts is None:
            state_dicts = {}  
        self.afds = afds
        self.state_dicts = state_dicts

    def analyze(self, text):
        results = []
        errors = []
        i = 0
        while i < len(text):
            if text[i] == '"' and (i + 1 < len(text) and text[i + 1] != "\\\\"):
                result, i = self.handle_string(text, i)
                if result is not None:
                    results.append((result, "String"))
                else:
                    errors.append(f"Unfinished string at position {i}")
            elif text[i].isdigit():  
                num, i = self.handle_number(text, i)
                results.append((num, "Number"))
            elif text[i].isalpha() or text[i] == '_':  
                ident, i = self.handle_identifier(text, i)
                results.append((ident, "Identifier"))
            elif text[i].isspace():  
                i = self.handle_whitespace(text, i)
            elif text[i] in "+-*/()=.,;:{}[]<>!&|%^'@":  
                op, i = self.handle_operator(text, i)
                results.append((op, "Operator"))
            elif text[i] == '/' and i + 1 < len(text) and text[i + 1] == '/':  
                i = self.handle_single_line_comment(text, i + 2)
            elif text[i] == '/' and i + 1 < len(text) and text[i + 1] == '*':  
                i = self.handle_multi_line_comment(text, i + 2)
            else:  
                errors.append(f"Unknown character: {text[i]} at position {i}")
                i += 1
        if errors:
            error_message = "Errors found: " + " ".join(errors)
            results.append((error_message, "Error"))
        return results
    
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

    def handle_operator(self, text, i):
        return text[i], i + 1

    def handle_single_line_comment(self, text, i):
        while i < len(text) and text[i] != ' ':
            i += 1
        return i

    def handle_multi_line_comment(self, text, i):
        while i < len(text):
            if text[i] == '*' and i+1 < len(text) and text[i+1] == '/':
                return i + 2
            i += 1
        return i  

    def skip_single_line_comment(self, text, i):
        while i < len(text) and text[i] != '\\n':
            i += 1
        return i + 1

    def skip_multi_line_comment(self, text, i):
        while i + 1 < len(text):
            if text[i] == '*' and text[i + 1] == '/':
                return i + 2
            i += 1
        return i
'''
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(code)