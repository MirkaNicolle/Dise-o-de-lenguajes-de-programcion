import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import importlib.util

from generador_lexico import read_yalex_file, generate_lexical_analyzer_code
from generador_sintactico import parse_yapar_file, generate_sintactic_analyzer_code

class AnalysisApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.load_lex_button = tk.Button(self, text="Load Lexer", command=self.load_yalex)
        self.load_lex_button.pack(side="top")

        self.load_syn_button = tk.Button(self, text="Load Parser", command=self.load_yapar)
        self.load_syn_button.pack(side="top")

        self.load_file_button = tk.Button(self, text="Load Text File", command=self.load_text_file)
        self.load_file_button.pack(side="top")

        self.result_text = scrolledtext.ScrolledText(self, height=30, width=80)
        self.result_text.pack(side="bottom")

    def load_yalex(self):
        filepath = filedialog.askopenfilename(filetypes=[("YALex files", "*.yalex"), ("All files", "*.*")])
        if filepath:
            tokens = read_yalex_file(filepath)
            output_file = 'lexical_analyzer.py'
            generate_lexical_analyzer_code(tokens, output_file)
            self.load_module(output_file, 'lexical')

    def load_yapar(self):
        filepath = filedialog.askopenfilename(filetypes=[("YAPar files", "*.yalp"), ("All files", "*.*")])
        if filepath:
            grammar = parse_yapar_file(filepath)
            output_file = 'sintactic_analyzer.py'
            generate_sintactic_analyzer_code(grammar, output_file)
            self.load_module(output_file, 'sintactic')

    def load_text_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filepath:
            with open(filepath, 'r') as file:
                text = file.read()
            if self.lexical_analyzer:
                tokens = self.lexical_analyzer.analyze(text)
                self.display_results(tokens)
                if self.sintactic_analyzer:
                    self.run_sintactic_analysis(tokens)
            else:
                messagebox.showerror("Error", "Lexical analyzer not generated.")

    def load_module(self, module_path, type):
        spec = importlib.util.spec_from_file_location(module_path.replace('.py', ''), module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if type == 'lexical':
            self.lexical_analyzer = module.LexicalAnalyzer()  # Assuming LexicalAnalyzer does not require initialization arguments
            self.result_text.insert(tk.END, "Lexical analyzer generated and loaded successfully.\n")
        elif type == 'sintactic':
            self.sintactic_analyzer = module.Parser(self.lexical_analyzer)
            self.result_text.insert(tk.END, "Sintactic analyzer generated and loaded successfully.\n")

    def display_results(self, tokens):
        self.result_text.insert(tk.END, "Analyzing text...\n")
        for token in tokens:
            self.result_text.insert(tk.END, f"{token.type}: {token.value}\n")

    def run_sintactic_analysis(self, tokens):
        if not self.sintactic_analyzer:
            messagebox.showerror("Error", "Sintactic analyzer not loaded.")
            return
        self.sintactic_analyzer.set_tokens(tokens)
        try:
            parsed_result = self.sintactic_analyzer.parse_expression()
            self.result_text.insert(tk.END, f"\nParsed structure:\n{parsed_result}")
        except Exception as e:
            messagebox.showerror("Error", f"Syntactic analysis failed: {e}")
            self.result_text.insert(tk.END, f"Error: {str(e)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalysisApp(master=root)
    app.mainloop()