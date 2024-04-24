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
    """
    Genera el código fuente del analizador léxico a partir de los AFDs minimizados.
    Incluye todo el código necesario para que funcione de manera independiente.
    """
    with open(output_file, 'w') as file:
        file.write('# -*- coding: utf-8 -*-\n')
        file.write('class LexicalAnalyzer:\n')
        file.write('    def __init__(self):\n')
        file.write('        self.afds = {}\n')
        file.write('        self.state_dicts = {}\n')
        
        # Asegurarse de que todas las funciones de manejo de tokens están definidas aquí.
        file.write('''

    self.token_functions = {
            'number': self.handle_number,
            'identifier': self.handle_identifier,
            'whitespace': self.handle_whitespace,
            'operator': self.handle_operator
        }
    
    def handle_number(self, text):
        num = ''
        i = 0
        while i < len(text) and text[i].isdigit():
            num += text[i]
            i += 1
        return int(num)

    def handle_identifier(self, text):
        ident = ''
        i = 0
        while i < len(text) and (text[i].isalpha() or text[i] == '_'):
            ident += text[i]
            i += 1
        return ident.upper()

    def handle_whitespace(self, text):
        return None  # Ignore whitespaces

    def handle_operator(self, char):
        return char
''')
        for token, regex in tokens.items():
            afd = process_regex_to_afd(regex)
            start_state_id, state_dict = afd_to_dict(afd)
            file.write(f'        self.afds["{token}"] = {start_state_id}\n')
            file.write(f'        self.state_dicts["{token}"] = {state_dict}\n')
        
        file.write('''
    def analyze(self, text):
        results = {}
        current_tokens = {token: [] for token in self.afds}  # Acumular texto para cada token

        # Recorrer cada carácter del texto
        for index, char in enumerate(text):
            for token, state in list(current_tokens.items()):
                transitions = self.state_dicts[token][state]['transitions']
                if char in transitions:
                    next_state = transitions[char][0]
                    current_tokens[token].append(char)  # Acumular caracteres para este token
                    if self.state_dicts[token][next_state]['accept']:
                        # Si alcanza un estado de aceptación, guarda el token
                        token_text = ''.join(current_tokens[token])
                        if token not in results:
                            results[token] = []
                        results[token].append(token_text)
                        current_tokens[token] = []  # Reiniciar acumulador para este token
                else:
                    # Reiniciar si no hay transición válida
                    current_tokens[token] = []

        return results
''')

def main():
    tokens = read_yalex_file('especificaciones.yalex')
    generate_lexical_analyzer_code(tokens, 'lexical_analyzer.py')

if __name__ == '__main__':
    main()