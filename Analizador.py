'''Laboratorio D'''

from ShuntingYard import to_postfix
from Thompson import regex_to_afn
from Subconjuntos import afn_to_afd
from Minimizacion import minimize_afd

def read_yalex_file(file_path):
    """
    Lee un archivo YALex y extrae los tokens y sus expresiones regulares.
    """
    tokens = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':=' in line:
                token_name, regex = line.split(':=')
                tokens[token_name.strip()] = regex.strip()
    return tokens

def process_regex_to_afd(regex):
    """
    Convierte una expresión regular en su AFD minimizado correspondiente.
    """
    print(f"Processing regex to AFD: '{regex}'")
    postfix = to_postfix(regex)
    print(f"Postfix notation: '{postfix}'")
    afn = regex_to_afn(postfix)
    print("AFN states and transitions:")
    for state in afn.states:
        print(f"  State {id(state)}: Accept={state.accept}, Transitions={state.transitions}")
    
    afd = afn_to_afd(afn)
    minimized_afd = minimize_afd(afd)
    print("Minimized AFD states and transitions:")
    for state in minimized_afd.states:
        transitions = {k: [id(s) for s in v] for k, v in state.transitions.items()}
        print(f"  State {id(state)}: Accept={state.accept}, Transitions={transitions}")
    
    return minimized_afd

def afd_to_dict(afd):
    """
    Convierte un objeto AFD en un diccionario para su uso en el analizador léxico.
    """
    state_dict = {}
    for state in afd.states:
        state_id = id(state)
        if state_id not in state_dict:
            state_dict[state_id] = {'accept': state.accept, 'transitions': {}}
        for symbol, states in state.transitions.items():
            state_dict[state_id]['transitions'][symbol] = [id(s) for s in states]
    start_state_id = id(afd.start_state)
    return start_state_id, state_dict

def generate_lexical_analyzer_code(tokens, output_file):
    """
    Genera el código fuente del analizador léxico a partir de los AFDs minimizados.
    """
    with open(output_file, 'w') as file:
        file.write('# -*- coding: utf-8 -*-\n')
        file.write('class LexicalAnalyzer:\n')
        file.write('    def __init__(self):\n')
        file.write('        self.afds = {}\n')
        file.write('        self.state_dicts = {}\n')
        
        for token, regex in tokens.items():
            afd = process_regex_to_afd(regex)
            start_state_id, state_dict = afd_to_dict(afd)
            file.write(f'        self.afds["{token}"] = {start_state_id}\n')
            file.write(f'        self.state_dicts["{token}"] = {state_dict}\n')
        
        file.write('''
    def is_in_range(self, char, range_spec):
        if '-' in range_spec:
            # Reemplaza los corchetes para no interferir con la lógica del rango
            range_spec = range_spec.replace('[', '').replace(']', '')
            # Itera sobre cada sub-rango separado por un guión
            ranges = range_spec.split('-')
            last_char = ''
            for i, part in enumerate(ranges):
                if i == 0:  # Primer elemento
                    last_char = part
                else:
                    # Si es el último elemento o el siguiente comienza con un rango nuevo
                    if i == len(ranges) - 1 or ranges[i + 1][0].isalpha():
                        start, end = last_char, part
                        if start <= char <= end:
                            return True
                        last_char = part
                    else:
                        # Maneja un carácter independiente que termina con guión
                        if part == '':
                            if last_char == char:
                                return True
                        last_char = part
        else:
            return char in range_spec
        return False

    def analyze(self, text):
        results = {}
        print(f"Analyzing text: '{text}'")  # Muestra el texto que se está analizando
        for token, start_state_id in self.afds.items():
            for i in range(len(text)):
                state = start_state_id
                print(f"Starting new token search for '{token}' from position {i}")  # Indica la búsqueda de un nuevo token
                for j in range(i, len(text)):
                    char = text[j]
                    transitions = self.state_dicts[token][state]["transitions"]
                    next_state = None
                    print(f"  At state {state}, processing char '{char}'")  # Muestra el carácter actual y el estado
                    for range_spec, states in transitions.items():
                        if self.is_in_range(char, range_spec):
                            next_state = states[0]
                            print(f"    Found valid transition for '{char}' in range '{range_spec}'; moving to state {next_state}")  # Muestra transición válida
                            break
                    if next_state is None:
                        print(f"    No valid transition found for '{char}'; stopping search from position {i}")  # No se encontraron transiciones válidas
                        break
                    state = next_state
                    if self.state_dicts[token][state]["accept"]:
                        matched_text = text[i:j+1]
                        print(f"    Token '{token}' recognized: '{matched_text}' at position {i}-{j}")  # Muestra reconocimiento de token
                        if token not in results:
                            results[token] = []
                        results[token].append(matched_text)
                        break
        return results

analyzer = LexicalAnalyzer()
print(analyzer.analyze("abc"))
''')

def main():
    tokens = read_yalex_file('easy.yalex')
    generate_lexical_analyzer_code(tokens, 'lexical_analyzer.py')

if __name__ == '__main__':
    main()