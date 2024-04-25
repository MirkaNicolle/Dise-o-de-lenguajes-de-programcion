'''Laboratorio D'''

from ShuntingYard import to_postfix
from Thompson import regex_to_afn
from Subconjuntos import afn_to_afd
from Minimizacion import minimize_afd

def read_yalex_file(file_path):
    tokens = {}
    with open(file_path, 'r') as file:
        '''for line in file:
            if ':=' in line:
                token_name, regex = line.split(':=')
                tokens[token_name.strip()] = regex.strip()'''
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
class LexicalAnalyzer:
    def __init__(self, afds=None, state_dicts=None):
        self.afds = afds or {}
        self.state_dicts = state_dicts or {}

    def analyze(self, text):
        results = []
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
            elif text[i] in "+-*/()":
                op, i = self.handle_operator(text, i)
                results.append((op, "Operator"))
            else:
                raise ValueError(f"Unknown character: {text[i]}")
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
'''
    with open(output_file, 'w') as file:
        file.write(code)

'''def main():
    tokens = read_yalex_file('especificaciones.yalex')
    generate_lexical_analyzer_code(tokens, 'lexical_analyzer.py')

if __name__ == '__main__':
    main()'''