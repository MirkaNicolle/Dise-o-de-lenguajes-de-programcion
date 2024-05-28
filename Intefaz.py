import tkinter as tk
from tkinter import filedialog, Text, messagebox

from generador_lexico import LexicalAnalyzer
from generador_sintactico import Parser
from generadores import parse_yapar_file, read_yalex_file, run_analysis  # Importa run_analysis
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
            self.clear_output_area()
            self.process_text(input_text)

    def clear_output_area(self):
        self.output_area.delete('1.0', tk.END)

    def process_text(self, input_text):
        yalex_path = 'hard_especificaciones.yalex'
        yapar_path = 'especificaciones_yapar.yalp'

        self.clear_output_area()  # Limpia el área de salida antes de procesar el nuevo archivo

        output = run_analysis(input_text, yalex_path, yapar_path)
        self.output_area.insert(tk.END, output)

        self.grammar = parse_yapar_file(yapar_path)  # Asegúrate de que self.grammar se inicialice aquí

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