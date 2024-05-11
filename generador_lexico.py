'''Laboratorio D'''

# -*- coding: utf-8 -*-
from ShuntingYard import to_postfix
from Thompson import regex_to_afn
from Subconjuntos import afn_to_afd
from Minimizacion import minimize_afd

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

def process_regex_to_afd(regex):
    postfix = to_postfix(regex) # Conversión de expresión regular en notación postfix
    afn = regex_to_afn(postfix) # Generación de AFN
    afd = afn_to_afd(afn) # Conversión de AFN a AFD
    minimized_afd = minimize_afd(afd) # Minimización de AFD
    return minimized_afd 

def afd_to_dict(afd):
    state_dict = {}
    for state in afd.states:
        state_id = id(state)
        state_dict[state_id] = {'accept': state.accept, 'transitions': {}}
        for symbol, states in state.transitions.items():
            state_dict[state_id]['transitions'][symbol] = [id(s) for s in states]
    start_state_id = id(afd.start_state)
    return start_state_id, state_dict

def generate_lexical_analyzer_code(tokens, output_file): #codigo fuente para analizador lexico
    code = '''
# -*- coding: utf-8 -*-
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return f"{self.type}: {self.value}"
    
class LexicalAnalyzer:
    def __init__(self, input_text=None):
        self.input = input_text
        self.current_position = 0
        self.total_length = len(input_text) if input_text else 0

    def set_input(self, input_text):
        self.input = input_text
        self.current_position = 0
        self.total_length = len(input_text)

    def get_next_token(self):
        while self.current_position < self.total_length:
            if self.input[self.current_position].isspace():
                self.current_position += 1
                continue

            if self.input[self.current_position] == '/':
                # Check for single line comment
                if self.current_position + 1 < self.total_length and self.input[self.current_position + 1] == '/':
                    self.skip_single_line_comment()
                    continue
                # Check for multi line comment
                elif self.current_position + 1 < self.total_length and self.input[self.current_position + 1] == '*':
                    self.skip_multi_line_comment()
                    continue

            if self.input[self.current_position].isdigit():
                return self.get_number()

            if self.input[self.current_position].isalpha() or self.input[self.current_position] == '_':
                return self.get_identifier()

            if self.input[self.current_position] in "+-*/()=.,;:{}[]<>!&|%^'@":
                return self.get_operator()
        
        return None

    def analyze(self, text):
        results = []
        errors = []
        i = 0
        while i < len(text):
            if text[i] == '"' and (i + 1 < len(text) and text[i + 1] != "\\\\"):
                result, i = self.handle_string(text, i)
                if result is not None:
                    results.append(Token("String", result))
            elif text[i].isdigit():
                num, i = self.handle_number(text, i)
                results.append(Token("Number", num))
            elif text[i].isalpha() or text[i] == '_':
                ident, i = self.handle_identifier(text, i)
                results.append(Token("Identifier", ident))
            elif text[i].isspace():
                i = self.handle_whitespace(text, i)
            elif text[i] in "+-*/()=.,;:{}[]<>!&|%^'@":
                op, i = self.handle_operator(text, i)
                results.append(Token("Operator", op))
            elif text[i] == '/' and i + 1 < len(text) and text[i + 1] == '/':
                i = self.handle_single_line_comment(text, i + 2)
            elif text[i] == '/' and i + 1 < len(text) and text[i + 1] == '*':
                i = self.handle_multi_line_comment(text, i + 2)
            else:
                errors.append(f"Unknown character: {text[i]} at position {i}")
                i += 1
        if errors:
            results.append(Token("Error", " ".join(errors)))
        return results
    
    def skip_whitespace(self):
        while self.current_position < self.total_length and self.input[self.current_position].isspace():
            self.current_position += 1
    
    def handle_string(self, text, i):
        if text[i] == '"' and (i == 0 or text[i-1] != '\\\\'):  # Comienza una nueva cadena si no está escapada
            i += 1
            start = i
            while i < len(text):
                if text[i] == '"' and text[i-1] != '\\\\':  # Finaliza si encuentra una comilla no escapada
                    return text[start:i], i + 1
                i += 1
            return text[start:], i  # Retorna lo que pueda si no encuentra el final
        return None, i
    
    def get_number(self):
        start_position = self.current_position
        has_decimal = False
        while self.current_position < self.total_length and (self.input[self.current_position].isdigit() or (self.input[self.current_position] == '.' and not has_decimal)):
            if self.input[self.current_position] == '.':
                has_decimal = True
            self.current_position += 1
        value = self.input[start_position:self.current_position]
        token_type = 'FLOAT' if '.' in value else 'NUMBER'
        return {'type': token_type, 'value': value}


    def get_identifier(self):
        start_position = self.current_position
        while self.current_position < self.total_length and (self.input[self.current_position].isalpha() or self.input[self.current_position] == '_'):
            self.current_position += 1
        value = self.input[start_position:self.current_position].upper()
        return {'type': 'IDENTIFIER', 'value': value}

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
        return {'type': 'OPERATOR', 'value': operator}

    def handle_single_line_comment(self, text, i):
        while i < len(text) and text[i] != ' ':
            i += 1
        return i

    def handle_multi_line_comment(self, text, i):
        while i < len(text):
            if text[i] == '*' and i+1 < len(text) and text[i+1] == '//':
                return i + 2
            i += 1
        return i  

    def skip_single_line_comment(self):
        while self.current_position < self.total_length and self.input[self.current_position] != '\\n':
            self.current_position += 1

    def skip_multi_line_comment(self):
        self.current_position += 2  # Skip the initial /*
        while self.current_position + 1 < self.total_length:
            if self.input[self.current_position] == '*' and self.input[self.current_position + 1] == '/':
                self.current_position += 2  # Skip past the */
                break
            self.current_position += 1
'''
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(code)

def main():
    file_path_yalex = 'hard_especificaciones.yalex'  # Asegúrate de que la ruta al archivo YALex sea correcta
    rules = read_yalex_file(file_path_yalex)  # Carga las definiciones de tokens

    # Especifica un nombre de archivo de salida para el código del analizador léxico generado
    output_file = 'lexical_analyzer.py'
    generate_lexical_analyzer_code(rules, output_file)

if __name__ == "__main__":
    main()