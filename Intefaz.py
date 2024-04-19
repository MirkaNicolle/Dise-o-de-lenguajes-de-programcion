import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Text
from ShuntingYard import to_postfix
from Thompson import main as thompson_main
from Subconjuntos import main as subsets_main
from Minimizacion import main as minimization_main
import os

class LexicalAnalyzer:
    def __init__(self, master):
        self.master = master
        self.file_path = ""  # Para rastrear el archivo cargado
        self.setup_gui()
        self.postfix_output = "output_postfix.yalex"
        self.thompson_output = "diagraph_thompson.txt"
        self.subsets_output = "diagraph_subsets.txt"
        self.minimization_output = "diagraph_minimization.txt"

    def setup_gui(self):
        self.master.title("Analizador léxico: YALex")
        self.master.configure(bg="#282a36")
        self.master.geometry('1200x800')  # Aumentado el tamaño de la ventana
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 12, 'bold'), background="#44475a", foreground="#f8f8f2")
        style.configure('TLabel', font=('Helvetica', 14, 'bold'), background="#282a36", foreground="#f8f8f2")
        style.configure('TText', font=('Helvetica', 12, 'normal'), background="#6272a4", foreground="#f8f8f2")

        ttk.Label(self.master, text="Analizador léxico: YALex", style='TLabel').pack(pady=(20, 5))
        ttk.Label(self.master, text="Seleccione el archivo a procesar", style='TLabel').pack(pady=(0, 20))
        ttk.Button(self.master, text="Cargar Archivo YALex", command=self.load_file, style='TButton').pack()
        ttk.Button(self.master, text="Convertir a Postfix", command=self.convert_to_postfix, style='TButton').pack(pady=5)
        ttk.Button(self.master, text="Algoritmo de Thompson", command=lambda: self.run_algorithm(thompson_main, self.thompson_output), style='TButton').pack(pady=5)
        ttk.Button(self.master, text="Subconjuntos AFD", command=lambda: self.run_algorithm(subsets_main, self.subsets_output), style='TButton').pack(pady=5)
        ttk.Button(self.master, text="Minimización AFD", command=lambda: self.run_algorithm(minimization_main, self.minimization_output), style='TButton').pack(pady=5)
        self.log = Text(self.master, height=100, width=200, state='disabled', wrap='word', font=('Helvetica', 10, 'normal'))
        self.log.pack(pady=(10, 20))

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("YALex files", "*.yalex"), ("All files", "*.*")])
        if self.file_path:
            self.log_message(f"Archivo cargado: {self.file_path}")

    def convert_to_postfix(self):
        if not self.file_path:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        # Implementar la conversión real a postfix aquí y guardar en self.postfix_output
        self.log_message("Archivo convertido a Postfix y guardado.")

    def run_algorithm(self, algorithm, output_file):
        if not self.file_path:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        algorithm(self.postfix_output, output_file)
        self.display_results(output_file)

    def display_results(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                results = file.read()
            self.log.config(state='normal')
            self.log.delete(1.0, tk.END)  # Borrar el contenido anterior
            self.log.insert(tk.END, results)
            self.log.config(state='disabled')
        except Exception as e:
            self.log_message(f"No se pudo leer el archivo de resultados: {str(e)}")

    def log_message(self, message):
        self.log.config(state='normal')
        self.log.insert(tk.END, message + "\n")
        self.log.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = LexicalAnalyzer(root)
    root.mainloop()