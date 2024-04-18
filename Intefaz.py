import tkinter as tk
from tkinter import filedialog, Label, Button, Text
from tkinter import messagebox
import os

class LexicalAnalyzer:
    def __init__(self, master):
        self.master = master
        master.title("Analizador léxico: YALex")

        background_color = "#282a36"
        text_color = "#f8f8f2"
        button_color = "#44475a"
        master.configure(bg=background_color)

        self.title_label = Label(master, text="Analizador léxico: YALex", font=("Helvetica", 16, "bold"), bg=background_color, fg=text_color)
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = Label(master, text="Por favor seleccione el archivo a procesar", font=("Helvetica", 14), bg=background_color, fg=text_color)
        self.subtitle_label.pack(pady=(0, 20))

        self.load_button = Button(master, text="Cargar Archivo YALex", command=self.load_file, bg=button_color, fg=text_color)
        self.load_button.pack()

        # Botones para cada acción
        self.postfix_button = Button(master, text="Convertir a Postfix", command=self.convert_to_postfix, bg=button_color, fg=text_color)
        self.postfix_button.pack(pady=5)

        self.thompson_button = Button(master, text="Algoritmo de Thompson", command=self.run_thompson, bg=button_color, fg=text_color)
        self.thompson_button.pack(pady=5)

        self.subsets_button = Button(master, text="Subconjuntos AFD", command=self.run_subsets, bg=button_color, fg=text_color)
        self.subsets_button.pack(pady=5)

        self.minimization_button = Button(master, text="Minimización AFD", command=self.run_minimization, bg=button_color, fg=text_color)
        self.minimization_button.pack(pady=5)

        self.log = Text(master, height=10, state='disabled', bg="#6272a4", fg=text_color)
        self.log.pack(pady=(0, 20))

        self.image_label = Label(master)
        self.image_label.pack()

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("YALex files", "*.yalex"), ("All files", "*.*")])
        if self.file_path:
            self.log_message(f"Archivo cargado: {self.file_path}")
        else:
            self.log_message("Carga de archivo cancelada.")

    def convert_to_postfix(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        self.log_message("Convirtiendo a Postfix...")
        # Aquí debes agregar la lógica para leer el archivo, convertir a postfix y visualizar/guardar los resultados.

    def run_thompson(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        self.log_message("Ejecutando Thompson...")
        # Implementar la lógica similar a la descripción anterior.

    def run_subsets(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        self.log_message("Ejecutando Subconjuntos...")
        # Implementar la lógica para convertir AFN a AFD y visualizar.

    def run_minimization(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        self.log_message("Ejecutando Minimización...")
        # Implementar la lógica para minimizar AFD y visualizar.

    def log_message(self, message):
        self.log.config(state='normal')
        self.log.insert(tk.END, message + "\n")
        self.log.config(state='disabled')

    def show_image(self, image_path):
        try:
            if os.path.exists(image_path):
                photo = tk.PhotoImage(file=image_path)
                self.image_label.configure(image=photo)
                self.image_label.image = photo
            else:
                self.log_message(f"No se encontró la imagen: {image_path}")
        except Exception as e:
            self.log_message(f"Error al cargar la imagen: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LexicalAnalyzer(root)
    root.mainloop()