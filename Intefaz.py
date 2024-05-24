import tkinter as tk
from tkinter import filedialog, Text, messagebox

from generador_lexico import LexicalAnalyzer
from generador_sintactico import Parser
from generadores import parse_yapar_file, read_yalex_file
from automaton import LR0Automaton
from visualizacion import visualize_automaton

class MainApplication:
    def __init__(self, root):
        self.root = root
        root.title("Laboratorio E")
        root.geometry("800x600")
        root.configure(bg='#b3d9ff')

        self.output_area = Text(root, height=20, width=80, bg="#e6f2ff")
        self.output_area.pack(pady=20)

        button_frame = tk.Frame(root, bg='#b3d9ff')
        button_frame.pack(fill=tk.X, pady=10)

        open_file_button = tk.Button(button_frame, text="Cargar Archivo", font=('Helvetica', 12), padx=20, pady=10, fg="white", bg="#3399ff", command=self.open_file)
        open_file_button.pack(side=tk.LEFT, padx=20, expand=True)

        run_automaton_button = tk.Button(button_frame, text="Generar Autómata LR(0)", font=('Helvetica', 12), padx=20, pady=10, fg="white", bg="#3399ff", command=self.generate_automaton)
        run_automaton_button.pack(side=tk.LEFT, padx=20, expand=True)

        self.grammar = None
        self.automaton = None

    def open_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Seleccionar Archivo", filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        if filename:
            input_text = self.read_file(filename)
            self.process_text(input_text)

    def process_text(self, input_text):
        yalex_path = 'hard_especificaciones.yalex'
        yapar_path = 'especificaciones_yapar.yalp'

        lexical_rules = read_yalex_file(yalex_path)
        self.grammar = parse_yapar_file(yapar_path)  

        lexical_analyzer = LexicalAnalyzer(lexical_rules)
        lexical_analyzer.set_input(input_text)
        tokens = []
        self.output_area.insert(tk.END, "Generated Tokens:\n")
        while True:
            token = lexical_analyzer.get_next_token()
            if token is None:
                break
            tokens.append(token)
            self.output_area.insert(tk.END, f"Token: Type={token.type}, Value={token.value}\n")

        parser = Parser(tokens)
        try:
            parse_tree = parser.parse()
            self.output_area.insert(tk.END, "\nSyntactic Analysis:\n")
            self.output_area.insert(tk.END, str(parse_tree) + "\n")
            self.parse_tree = parse_tree  
        except Exception as e:
            self.output_area.insert(tk.END, f"Error parsing: {e}\n")

    def generate_automaton(self):
        if self.grammar:
            try:
                self.automaton = LR0Automaton(self.grammar)
                dot = visualize_automaton(self.automaton)
                dot.render('lr0_automaton', view=True)
                self.output_area.insert(tk.END, "Autómata LR(0) generado y visualizado correctamente.\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate automaton: {e}")
        else:
            messagebox.showerror("Error", "Grammar not loaded. Please load a file and validate syntax first.")

    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

root = tk.Tk()
app = MainApplication(root)
root.mainloop()