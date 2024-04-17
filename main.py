from tkinter import Tk
from Intefaz import LexicalAnalyzer

def read_yalex_file(file_path):
    """Lee un archivo YALex y devuelve un diccionario con tokens y sus expresiones regulares."""
    tokens = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip() and ':=' in line:
                    token_name, regex = line.split(':=')
                    tokens[token_name.strip()] = regex.strip()
    except FileNotFoundError:
        print(f"El archivo {file_path} no fue encontrado.")
    return tokens

def process_tokens(tokens):
    """Procesa cada token y su expresión regular, convirtiéndolos en AFNs, AFDs y visualizando los resultados."""
    from Thompson import regex_to_afn, visualize_afn
    from Subconjuntos import afn_to_afd, visualize_automaton as visualize_dfa
    from Minimizacion import minimize_afd, visualize_automaton as visualize_minimized_dfa

    for token_name, regex in tokens.items():
        afn = regex_to_afn(regex)
        if afn:
            visualize_afn(afn, f"AFN_{token_name}.png")
            dfa = afn_to_afd(afn)
            visualize_dfa(dfa, f"DFA_{token_name}.png")
            minimized_dfa = minimize_afd(dfa)
            visualize_minimized_dfa(minimized_dfa, f"Minimized_DFA_{token_name}.png")
        else:
            print(f"Error al procesar la regex para el token: {token_name}")

if __name__ == '__main__':
    root = Tk()
    app = LexicalAnalyzer(root)
    root.mainloop()

'''def read_yalex_file(file_path):
    tokens = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and ':=' in line:
                token_name, regex = line.split(':=')
                tokens[token_name.strip()] = regex.strip()
    return tokens

# Prueba de la función de lectura
tokens = read_yalex_file('easy.yalex')
print("Tokens leídos:", tokens)'''
