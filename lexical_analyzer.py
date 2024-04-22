# -*- coding: utf-8 -*-
class LexicalAnalyzer:
    def __init__(self):
        self.afds = {}
        self.state_dicts = {}
        self.afds["NUMERO"] = 2471446831248
        self.state_dicts["NUMERO"] = {2471446831248: {'accept': False, 'transitions': {'0-9': [2471446830928]}}}
        self.afds["IDENTIFICADOR"] = 2471446832016
        self.state_dicts["IDENTIFICADOR"] = {2471446832016: {'accept': False, 'transitions': {'a-zA-Z_': [2471446832208]}}}

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
