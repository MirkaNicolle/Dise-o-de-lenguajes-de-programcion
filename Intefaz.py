import tkinter as tk
from tkinter import filedialog, Label, Button, Text
from tkinter import messagebox
from Thompson import regex_to_afn, visualize_afn
from Subconjuntos import afn_to_afd, visualize_automaton as visualize_afd
from Minimizacion import minimize_afd, visualize_automaton as visualize_minimized_afd
import os

class LexicalAnalyzer:
    def __init__(self, master):
        self.master = master
        master.title("Analizador léxico: YALex")

        # Configuración de colores y estilo
        background_color = "#282a36"
        text_color = "#f8f8f2"
        button_color = "#44475a"
        master.configure(bg=background_color)

        # Título y subtítulo
        self.title_label = Label(master, text="Analizador léxico: YALex", font=("Helvetica", 16, "bold"), bg=background_color, fg=text_color)
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = Label(master, text="Por favor seleccione el archivo a procesar", font=("Helvetica", 14), bg=background_color, fg=text_color)
        self.subtitle_label.pack(pady=(0, 20))

        # Botón para cargar archivo
        self.load_button = Button(master, text="Cargar Archivo YALex", command=self.load_file, bg=button_color, fg=text_color)
        self.load_button.pack()

        # Botón para procesar el archivo
        self.process_button = Button(master, text="Procesar", command=self.process_file, bg=button_color, fg=text_color)
        self.process_button.pack(pady=20)

        # Área de log
        self.log = Text(master, height=10, state='disabled', bg="#6272a4", fg=text_color)
        self.log.pack(pady=(0, 20))

        # Configuración de la visualización
        self.image_label = Label(master)
        self.image_label.pack()

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("YALex files", "*.yalex"), ("All files", "*.*")])
        if self.file_path:
            self.log_message(f"Archivo cargado: {self.file_path}")
        else:
            self.log_message("Carga de archivo cancelada.")

    def process_file(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return

        self.log_message("Procesando archivo...")
        afn = regex_to_afn(self.file_path)
        if afn:
            visualize_afn(afn)  # Visualizar el AFN generado
            self.show_image("Thompson_AFN.png")

            dfa = afn_to_afd(afn)
            visualize_afd(dfa, "Subconjuntos_AFD")
            self.show_image("Subconjuntos_AFD.png")

            minimized_dfa = minimize_afd(dfa)
            visualize_minimized_afd(minimized_dfa, "Minimized_AFD")
            self.show_image("Minimized_AFD.png")

            self.log_message("Proceso completado. AFD minimizado visualizado.")
        else:
            self.log_message("Error al procesar el archivo.")

    def show_image(self, image_path):
        try:
            if os.path.exists(image_path):
                photo = tk.PhotoImage(file=image_path)
                self.image_label.configure(image=photo)
                self.image_label.image = photo  # keep a reference!
            else:
                self.log_message(f"No se encontró la imagen: {image_path}")
        except Exception as e:
            self.log_message(f"Error al cargar la imagen: {str(e)}")


    def log_message(self, message):
        self.log.config(state='normal')
        self.log.insert(tk.END, message + "\n")
        self.log.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = LexicalAnalyzer(root)
    root.mainloop()