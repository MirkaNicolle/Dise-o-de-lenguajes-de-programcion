import tkinter as tk 
from tkinter import filedialog, messagebox, ttk, Text  
from ShuntingYard import to_postfix 
from Thompson import main as thompson_main 
from Subconjuntos import main as subsets_main  
from Minimizacion import main as minimization_main 

class LexicalAnalyzer:  #clase para el analizador lexico
    def __init__(self, master):  
        self.master = master  #asignar el master (root de Tkinter)
        self.file_path = ""  #inicializar la ruta del archivo
        self.setup_gui()  #configuracion interfaz grafica
        self.postfix_output = "output_postfix.yalex"  #rutas
        self.thompson_output = "diagraph_thompson.txt"  
        self.subsets_output = "diagraph_subsets.txt"  
        self.minimization_output = "diagraph_minimization.txt" 

    def setup_gui(self):  #configurar la interfaz grafica
        self.master.title("Analizador léxico: YALex")  
        self.master.configure(bg="#282a36")  
        self.master.geometry('1200x800')  #tamano de la ventana
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

    def load_file(self):  #carga de archivo
        self.file_path = filedialog.askopenfilename(filetypes=[("YALex files", "*.yalex"), ("All files", "*.*")])  #seleccion de archivo
        if self.file_path: 
            self.log_message(f"Archivo cargado: {self.file_path}") 

    def convert_to_postfix(self):  #postfix
        if not self.file_path: 
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.") 
            return
        self.log_message("Archivo convertido a Postfix y guardado.")

    def run_algorithm(self, algorithm, output_file):  #ejecucion de algoritmos
        if not self.file_path:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        algorithm(self.postfix_output, output_file)  #ejecucion del algoritmo seleccionado
        self.display_results(output_file)  # mostrar resultados

    def display_results(self, file_name):  #mostrar resultados
        try:
            with open(file_name, 'r', encoding='utf-8') as file:  #archivo de resultados
                results = file.read()  #leer resultados
            self.log.config(state='normal')  #habilitar area de texto
            self.log.delete(1.0, tk.END)  #borrar contenido anterior
            self.log.insert(tk.END, results)  #insertar resultados
            self.log.config(state='disabled')  #deshabilitar area de texto
        except Exception as e:
            self.log_message(f"No se pudo leer el archivo de resultados: {str(e)}")

    def log_message(self, message):  #mostrar mensajes en el log
        self.log.config(state='normal')  #habilitar area de texto
        self.log.insert(tk.END, message + "\n")  #mensaje
        self.log.config(state='disabled')  #deshabilitar area de texto

if __name__ == "__main__":  
    root = tk.Tk()  
    app = LexicalAnalyzer(root) 
    root.mainloop() 