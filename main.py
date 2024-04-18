from tkinter import Tk
from Intefaz import LexicalAnalyzer
from tkinter import filedialog, messagebox
from ShuntingYard import to_postfix
from Thompson import regex_to_afn, visualize_afn
from Subconjuntos import afn_to_afd, visualize_automaton as visualize_afd
from Minimizacion import minimize_afd, visualize_automaton as visualize_minimized_afd

def load_file(self):
    self.file_path = filedialog.askopenfilename(filetypes=[("YALex files", "*.yalex"), ("All files", "*.*")])
    if self.file_path:
        self.tokens = read_yalex_file(self.file_path)
        self.log_message(f"Archivo cargado: {self.file_path}")
    else:
        self.log_message("Carga de archivo cancelada.")

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

def convert_to_postfix(self):
    if not hasattr(self, 'tokens') or not self.tokens:
        messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
        return
    self.log_message("Convirtiendo a Postfix...")
    postfix_tokens = {name: to_postfix(regex) for name, regex in self.tokens.items()}
    for name, postfix in postfix_tokens.items():
        self.log_message(f"{name} en Postfijo: {postfix}")

def run_thompson(self):
    if not hasattr(self, 'tokens') or not self.tokens:
        messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
        return
    self.log_message("Ejecutando Thompson...")
    for name, regex in self.tokens.items():
        afn = regex_to_afn(regex)
        if afn:
            visualize_afn(afn, f"AFN_{name}.png")
            self.show_image(f"AFN_{name}.png")
        else:
            self.log_message(f"Error al generar el AFN para el token: {name}")

def run_subsets(self):
    self.log_message("Ejecutando Subconjuntos...")
    for name, regex in self.tokens.items():
        afn = regex_to_afn(regex)
        if afn:
            dfa = afn_to_afd(afn)
            visualize_afd(dfa, f"DFA_{name}.png")
            self.show_image(f"DFA_{name}.png")
        else:
            self.log_message(f"Error al generar el DFA para el token: {name}")

def run_minimization(self):
    self.log_message("Ejecutando Minimización...")
    for name, regex in self.tokens.items():
        afn = regex_to_afn(regex)
        if afn:
            dfa = afn_to_afd(afn)
            minimized_dfa = minimize_afd(dfa)
            visualize_minimized_afd(minimized_dfa, f"Minimized_DFA_{name}.png")
            self.show_image(f"Minimized_DFA_{name}.png")
        else:
            self.log_message(f"Error al minimizar el DFA para el token: {name}")

if __name__ == '__main__':
    root = Tk()
    app = LexicalAnalyzer(root)
    root.mainloop()