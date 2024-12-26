import tkinter as tk
import importlib.util
from Generador import read_yalex_file, generate_lexical_analyzer_code
from tkinter import filedialog, messagebox, scrolledtext, font

class LexicalApp:
    def __init__(self, master):
        self.master = master
        master.title("Lab D: Lexical Analyzer")
        master.configure(bg='#4B0082') 

        button_font = font.Font(family="Helvetica", size=12, weight="bold")

        self.load_yalex_button = tk.Button(master, text="Especificaciones YALex", command=self.load_yalex, #boton yalex
        bg='#D8BFD8', fg='black', font=button_font, relief='flat', bd=0,
        activebackground='#DA70D6', activeforeground='white')
        self.load_yalex_button.pack(pady=10, padx=10)
        self.load_yalex_button.bind("<Enter>", lambda e: e.widget.config(bg='#DA70D6')) 
        self.load_yalex_button.bind("<Leave>", lambda e: e.widget.config(bg='#D8BFD8'))  

        self.load_text_button = tk.Button(master, text=".txt a analizar", command=self.load_text_file, #boton archivo a analizar
        bg='#D8BFD8', fg='black', font=button_font, relief='flat', bd=0,
        activebackground='#DA70D6', activeforeground='white')
        self.load_text_button.pack(pady=10, padx=10)
        self.load_text_button.bind("<Enter>", lambda e: e.widget.config(bg='#DA70D6')) 
        self.load_text_button.bind("<Leave>", lambda e: e.widget.config(bg='#D8BFD8'))

        self.result_text = scrolledtext.ScrolledText(master, width=70, height=20, bg='white') #area de resultados
        self.result_text.pack(pady=10, padx=10)

    def load_yalex(self):
        filepath = filedialog.askopenfilename(filetypes=(("YALex files", "*.yalex"), ("All files", "*.*")))
        if not filepath:
            return
        self.result_text.delete('1.0', tk.END) #vacia la interfaz para el sigueinte resulatado
        self.result_text.insert(tk.END, "Generando analizador...\n")
        self.master.update()  #actualizacion de la interfaz
        tokens = read_yalex_file(filepath)
        output_file = "lexical_analyzer.py"
        generate_lexical_analyzer_code(tokens, output_file)
        importlib.invalidate_caches() #recarga el modulo para reflejar los cambios
        spec = importlib.util.spec_from_file_location("lexical_analyzer", output_file)
        lexical_analyzer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lexical_analyzer)
        self.analyzer = lexical_analyzer.LexicalAnalyzer()
        self.result_text.insert(tk.END, "Analizador listo! Cargue un archivo de texto para analizar.\n")

    def load_text_file(self):
        filepath = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if not filepath:
            return
        if not self.analyzer:
            messagebox.showerror("Error", "Se necesita analizador")
            return
        self.result_text.delete('1.0', tk.END) #vacia la interfaz para el sigueinte resulatado
        with open(filepath, 'r') as file:
            text = file.read()
        try:
            results = self.analyzer.analyze(text)
            self.display_results(results)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.result_text.insert(tk.END, "Error: " + str(e) + "\n")

    def display_results(self, results):
        self.result_text.delete('1.0', tk.END)  
        if not results:
            self.result_text.insert(tk.END, "Tokens no encontrados\n")
        else:
            self.result_text.insert(tk.END, "Tokens encontrados:\n\n") 
            for val, typ in results:
                if typ == "Error":
                    self.result_text.insert(tk.END, f"Error: {val}\n\n")  #mostrar errores separadamente
                else:
                    self.result_text.insert(tk.END, f"{typ}: {val}\n\n")  #mostrar tokens con un salto de línea adicional

root = tk.Tk()
app = LexicalApp(root)
root.mainloop()