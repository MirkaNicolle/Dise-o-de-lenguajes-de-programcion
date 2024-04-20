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
    postfix = to_postfix(regex)
    afn = regex_to_afn(postfix)
    afd = afn_to_afd(afn)
    minimized_afd = minimize_afd(afd)
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
            parts = range_spec.split('-')
            start, end = parts[0], parts[-1]  # Asegura tomar el rango correctamente si hay escape
            if len(start) > 1:  # Maneja caracteres especiales escapados, como \-
                start = start[-1]
            if len(end) > 1:
                end = end[-1]
            return start <= char <= end
        return char in range_spec

    def analyze(self, text):
        results = {}
        for token, start_state_id in self.afds.items():
            for i in range(len(text)):
                state = start_state_id
                for j in range(i, len(text)):
                    char = text[j]
                    transitions = self.state_dicts[token][state]["transitions"]
                    next_state = None
                    for range_spec, states in transitions.items():
                        if self.is_in_range(char, range_spec):
                            next_state = states[0]  # assuming deterministic transition to one next state
                            break
                    if next_state is None:
                        break
                    state = next_state
                    if self.state_dicts[token][state]["accept"]:
                        matched_text = text[i:j+1]
                        if token not in results:
                            results[token] = []
                        results[token].append(matched_text)
                        break
        return results
''')

def main():
    tokens = read_yalex_file('easy.yalex')
    generate_lexical_analyzer_code(tokens, 'lexical_analyzer.py')

if __name__ == '__main__':
    main()