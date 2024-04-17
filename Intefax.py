import tkinter as tk
from tkinter import filedialog
from Thompson import regex_to_afn, visualize_afn
from Subconjuntos import afn_to_afd, visualize_automaton as visualize_dfa
from Minimizacion import minimize_afd, visualize_automaton as visualize_minimized_dfa
import os

class LexicalAnalyzer:
    def __init__(self, master):
        self.master = master
        master.title("YALex Analyzer")

        # Botón para cargar archivo
        self.load_button = tk.Button(master, text="Cargar Archivo YALex", command=self.load_file)
        self.load_button.pack()

        # Botón para procesar el archivo
        self.process_button = tk.Button(master, text="Procesar", command=self.process_file)
        self.process_button.pack()

        # Área de log
        self.log = tk.Text(master, height=10, state='disabled')
        self.log.pack()

        # Configuración de la visualización
        self.image_label = tk.Label(master)
        self.image_label.pack()

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("YALex files", "*.yalex"), ("All files", "*.*")])
        if self.file_path:
            self.log_message(f"Archivo cargado: {self.file_path}")
        else:
            self.log_message("Carga de archivo cancelada.")

    def process_file(self):
        if not hasattr(self, 'file_path'):
            self.log_message("Por favor, cargue un archivo primero.")
            return

        self.log_message("Procesando archivo...")
        # Asumiendo una función adaptada que procesa directamente desde el archivo
        afn = regex_to_afn(self.file_path)
        if afn:
            visualize_afn(afn)  # Visualizar el AFN generado
            self.show_image("Thompson_AFN.png")  # Asumiendo que visualize_afn guarda un archivo así

            dfa = afn_to_afd(afn)
            visualize_dfa(dfa, "Subconjuntos_DFA")  # Visualizar el DFA generado
            self.show_image("Subconjuntos_DFA.png")

            minimized_dfa = minimize_afd(dfa)
            visualize_minimized_dfa(minimized_dfa, "Minimized_DFA")  # Visualizar el DFA minimizado
            self.show_image("Minimized_DFA.png")

            self.log_message("Proceso completado. DFA minimizado visualizado.")
        else:
            self.log_message("Error al procesar el archivo.")

    def show_image(self, image_path):
        if os.path.exists(image_path):
            photo = tk.PhotoImage(file=image_path)
            self.image_label.configure(image=photo)
            self.image_label.image = photo  # keep a reference!
        else:
            self.log_message("No se encontró la imagen resultante.")

    def log_message(self, message):
        self.log.config(state='normal')
        self.log.insert(tk.END, message + "\n")
        self.log.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = LexicalAnalyzer(root)
    root.mainloop()