# -*- coding: utf-8 -*-
class LexicalAnalyzer:
    def __init__(self):
        self.afds = {}
        self.state_dicts = {}
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

    def analyze(self, text):
        results = {}
        current_tokens = {token: [] for token in self.afds}  # Acumular texto para cada token

        # Recorrer cada car�cter del texto
        for index, char in enumerate(text):
            for token, state in list(current_tokens.items()):
                transitions = self.state_dicts[token][state]['transitions']
                if char in transitions:
                    next_state = transitions[char][0]
                    current_tokens[token].append(char)  # Acumular caracteres para este token
                    if self.state_dicts[token][next_state]['accept']:
                        # Si alcanza un estado de aceptaci�n, guarda el token
                        token_text = ''.join(current_tokens[token])
                        if token not in results:
                            results[token] = []
                        results[token].append(token_text)
                        current_tokens[token] = []  # Reiniciar acumulador para este token
                else:
                    # Reiniciar si no hay transici�n v�lida
                    current_tokens[token] = []

        return results
