import os
import uuid
import tkinter as tk
from tkinter import filedialog, Text, messagebox

from automaton import LR0Automaton
from visualizacion import visualize_automaton
from parser_yapar import YaparParser
from slr_table import SLRTable

class MainApplication:
    def __init__(self, root):
        self.root = root
        root.title("Laboratorio F")
        root.geometry("1200x700")
        root.configure(bg='#003366') 

        self.output_area = Text(root, height=30, width=100, bg="#e6f2ff")
        self.output_area.pack(pady=20)

        button_frame = tk.Frame(root, bg='#003366')
        button_frame.pack(fill=tk.X, pady=10)

        open_yalex_button = tk.Button(button_frame, text="Cargar YALex", font=('Helvetica', 12), padx=20, pady=10, fg="white", bg="#3366cc", command=self.open_yalex_file)
        open_yalex_button.grid(row=0, column=0, padx=20, pady=10)

        open_yapar_button = tk.Button(button_frame, text="Cargar YAPar", font=('Helvetica', 12), padx=20, pady=10, fg="white", bg="#3366cc", command=self.open_yapar_file)
        open_yapar_button.grid(row=0, column=1, padx=20, pady=10)

        run_automaton_button = tk.Button(button_frame, text="Generar Autómata LR(0)", font=('Helvetica', 12), padx=20, pady=10, fg="white", bg="#3366cc", command=self.generate_automaton)
        run_automaton_button.grid(row=0, column=2, padx=20, pady=10)

        first_set_button = tk.Button(button_frame, text="Calcular Primero", font=('Helvetica', 12), padx=20, pady=10, fg="white", bg="#3366cc", command=self.calculate_first_sets)
        first_set_button.grid(row=1, column=0, padx=20, pady=10)

        follow_set_button = tk.Button(button_frame, text="Calcular Siguiente", font=('Helvetica', 12), padx=20, pady=10, fg="white", bg="#3366cc", command=self.calculate_follow_sets)
        follow_set_button.grid(row=1, column=1, padx=20, pady=10)

        slr_table_button = tk.Button(button_frame, text="Guardar Tabla SLR como PDF", font=('Helvetica', 12), padx=20, pady=10, fg="white", bg="#3366cc", command=self.save_slr_table_as_pdf)
        slr_table_button.grid(row=1, column=2, padx=20, pady=10)

        self.grammar = None
        self.automaton = None
        self.slr_table = None
        self.yalex_path = None
        self.yapar_path = None

    def open_yalex_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Seleccionar Archivo YALex", filetypes=(("YALex files", "*.yalex"), ("all files", "*.*")))
        if filename:
            self.yalex_path = filename
            self.output_area.insert(tk.END, f"Archivo YALex cargado: {filename}\n")

    def open_yapar_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Seleccionar Archivo YAPar", filetypes=(("YAPar files", "*.yalp"), ("all files", "*.*")))
        if filename:
            self.yapar_path = filename
            self.clear_output_area()  
            self.output_area.insert(tk.END, f"Archivo YAPar cargado: {filename}\n")
            self.process_yapar_file()

    def process_yapar_file(self):
        if self.yapar_path:
            yapar_parser = YaparParser(self.yapar_path)
            self.grammar = yapar_parser.get_grammar()
            self.output_area.insert(tk.END, "Gramática cargada correctamente.\n")
        else:
            messagebox.showerror("Error", "Debe cargar un archivo YAPar antes de continuar.")

    def clear_output_area(self):
        self.output_area.delete('1.0', tk.END)

    def delete_old_automaton_files(self):
        try:
            for file in os.listdir():
                if file.startswith("lr0_automaton"):
                    os.remove(file)
                    print(f"Deleted {file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete old automaton files: {e}")

    def generate_automaton(self):
        if self.grammar:
            try:
                self.delete_old_automaton_files()
                self.automaton = LR0Automaton(self.grammar)
                unique_filename = f'lr0_automaton_{uuid.uuid4()}'
                dot = visualize_automaton(self.automaton)
                dot.render(unique_filename, format='pdf', cleanup=True)
                self.output_area.insert(tk.END, f"Autómata LR(0) generado y visualizado correctamente. Archivo: {unique_filename}.pdf\n")
                os.system(f"start {unique_filename}.pdf")  
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate automaton: {e}")
        else:
            messagebox.showerror("Error", "Gramática no cargada. Por favor, cargue un archivo YAPar y valide la sintaxis primero.")

    def calculate_first_sets(self):
        if self.grammar:
            self.grammar.calculate_first_sets()
            first_sets = self.grammar.first_sets
            output = "\nConjuntos Primero:\n"
            for non_terminal, first_set in first_sets.items():
                output += f"{non_terminal}: {first_set}\n"
            self.output_area.insert(tk.END, output)
        else:
            messagebox.showerror("Error", "Gramática no cargada. Por favor, cargue un archivo YAPar y valide la sintaxis primero.")

    def calculate_follow_sets(self):
        if self.grammar:
            self.grammar.calculate_follow_sets()
            follow_sets = self.grammar.follow_sets
            output = "\nConjuntos Siguiente:\n"
            for non_terminal, follow_set in follow_sets.items():
                output += f"{non_terminal}: {follow_set}\n"
            self.output_area.insert(tk.END, output)
        else:
            messagebox.showerror("Error", "Gramática no cargada. Por favor, cargue un archivo YAPar y valide la sintaxis primero.")

    def save_slr_table_as_pdf(self):
        if self.grammar:
            self.slr_table = SLRTable(self.grammar)
            pdf_filename = 'slr_table.pdf'
            self.slr_table.save_slr_table_as_pdf(pdf_filename)
            self.output_area.insert(tk.END, f"Tabla SLR generada y guardada correctamente en archivo: {pdf_filename}\n")
            os.system(f"start {pdf_filename}")  
        else:
            messagebox.showerror("Error", "Gramática no cargada. Por favor, cargue un archivo YAPar y valide la sintaxis primero.")

    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

root = tk.Tk()
app = MainApplication(root)
root.mainloop()