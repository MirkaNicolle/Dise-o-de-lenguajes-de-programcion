import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import importlib.util
from Generador import read_yalex_file, generate_lexical_analyzer_code

class LexicalApp:
    def __init__(self, master):
        self.master = master
        master.title("Lexical Analyzer GUI")
        self.load_yalex_button = tk.Button(master, text="Load YALex Specifications", command=self.load_yalex)
        self.load_yalex_button.pack()
        self.load_text_button = tk.Button(master, text="Load Text File", command=self.load_text_file)
        self.load_text_button.pack()
        self.result_text = scrolledtext.ScrolledText(master, width=70, height=20)
        self.result_text.pack()
        self.analyzer = None

    def load_yalex(self):
        filepath = filedialog.askopenfilename(filetypes=(("YALex files", "*.yalex"), ("All files", "*.*")))
        if not filepath:
            return
        tokens = read_yalex_file(filepath)
        output_file = "lexical_analyzer.py"
        generate_lexical_analyzer_code(tokens, output_file)
        # Carga dinámica del módulo generado
        spec = importlib.util.spec_from_file_location("lexical_analyzer", output_file)
        lexical_analyzer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lexical_analyzer)
        self.analyzer = lexical_analyzer.LexicalAnalyzer()

    def load_text_file(self):
        filepath = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if not filepath:
            return
        if not self.analyzer:
            messagebox.showerror("Error", "Please generate the lexical analyzer first.")
            return
        with open(filepath, 'r') as file:
            text = file.read()
        try:
            results = self.analyzer.analyze(text)
            self.display_results(results)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.result_text.insert(tk.END, "Error: " + str(e) + "\n")

    def display_results(self, results):
        self.result_text.delete('1.0', tk.END)  # Limpia el área de texto antes de mostrar nuevos resultados
        if not results:
            self.result_text.insert(tk.END, "No tokens found.\n")
        else:
            formatted_results = "\n".join(f"{typ}: {val}" for val, typ in results)
            self.result_text.insert(tk.END, "Tokens:\n" + formatted_results + "\n")

root = tk.Tk()
app = LexicalApp(root)
root.mainloop()
