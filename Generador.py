'''Laboratorio D'''

# -*- coding: utf-8 -*-
from ShuntingYard import to_postfix
from Thompson import regex_to_afn
from Subconjuntos import afn_to_afd
from Minimizacion import minimize_afd

def read_yalex_file(file_path):
    tokens = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if ':=' in line:
                token_name, regex = line.split(':=')
                tokens[token_name.strip()] = regex.strip()
    return tokens

def process_regex_to_afd(regex):
    postfix = to_postfix(regex)
    afn = regex_to_afn(postfix)
    afd = afn_to_afd(afn)
    minimized_afd = minimize_afd(afd)
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

def generate_lexical_analyzer_code(tokens, output_file):
    code = '''
# -*- coding: utf-8 -*-
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
            if text[i].isdigit():
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
                i += 1  # Move past the unknown character
        if errors:
            error_message = "Errors found: " + " ".join(errors)
            results.append((error_message, "Error"))
        return results

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
            if i < len(text) - 1 and text[i] == '*' and text[i+1] == '/':
                return i + 2
            i += 1
        return i  # Handle case where comment is not closed
'''
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(code)