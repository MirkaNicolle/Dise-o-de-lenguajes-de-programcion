'''Laboratorio C'''

import tkinter as tk 
from tkinter import filedialog, messagebox, ttk, Text  
from ShuntingYard import to_postfix 
from Thompson import main as thompson_main 
from Subconjuntos import main as subsets_main  
from Minimizacion import main as minimization_main 

class LexicalAnalyzer:
    def __init__(self, master):
        self.master = master
        self.file_path = ""
        self.setup_gui()
        self.postfix_output = "output_postfix.yalex"
        self.thompson_output = "diagraph_thompson.txt"
        self.subsets_output = "diagraph_subsets.txt"
        self.minimization_output = "diagraph_minimization.txt"

    def setup_gui(self):
        # Configurar la interfaz grafica
        self.master.title("Analizador lexico: YALex")
        self.master.configure(bg="#282a36")
        self.master.geometry('600x300')
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 12, 'bold'), background="#44475a", foreground="#f8f8f2")
        style.configure('TLabel', font=('Helvetica', 14, 'bold'), background="#282a36", foreground="#f8f8f2")
        style.configure('TText', font=('Helvetica', 12, 'normal'), background="#6272a4", foreground="#f8f8f2")

        # Crear los elementos de la interfaz
        ttk.Label(self.master, text="Analizador lexico: YALex", style='TLabel').pack(pady=(20, 5))
        ttk.Label(self.master, text="Seleccione el archivo a procesar", style='TLabel').pack(pady=(0, 20))
        ttk.Button(self.master, text="Cargar Archivo YALex", command=self.load_file, style='TButton').pack()
        ttk.Button(self.master, text="Generar Mega Automata", command=self.combine_graphs, style='TButton').pack(pady=5)
        self.log = Text(self.master, height=10, width=60, state='disabled', wrap='word', font=('Helvetica', 10, 'normal'))
        self.log.pack(pady=(10, 20))

    def load_file(self):
        # Cargar el archivo YALex
        self.file_path = filedialog.askopenfilename(filetypes=[("YALex files", "*.yalex"), ("All files", "*.*")])
        if self.file_path:
            self.log_message(f"Archivo cargado: {self.file_path}")

    def log_message(self, message):
        # Mostrar mensajes en la interfaz
        self.log.config(state='normal')
        self.log.insert(tk.END, message + "\n")
        self.log.config(state='disabled')

    def combine_graphs(self):
        if not self.file_path:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return

        try:
            # Convertir a postfix
            postfix_expressions = []
            with open(self.file_path, 'r') as file:
                for line in file:
                    if ':=' in line:
                        token_name, regex = line.split(':=', 1)
                        postfix_regex = to_postfix(regex.strip())
                        postfix_expressions.append(f"{token_name.strip()} := {postfix_regex}")
            with open(self.postfix_output, 'w') as file:
                file.write('\n'.join(postfix_expressions))
            self.log_message("Archivo convertido a Postfix y guardado en " + self.postfix_output)
            
            # Ejecutar Thompson, Subconjuntos y Minimizacion
            thompson_main(self.postfix_output, self.thompson_output)
            subsets_main(self.postfix_output, self.subsets_output)
            minimization_main(self.postfix_output, self.minimization_output)

            # Crear el grafo combinado
            combined_graph = graphviz.Digraph(name="digraph_afd_combined")
            combined_graph.node('start', shape='point')  # Nodo principal de inicio

            def extract_and_rename_nodes(graph_file, prefix, node_offset):
                with open(graph_file, 'r') as f:
                    lines = f.readlines()
                    node_map = {}
                    edges = []
                    start_node = None
                    for line in lines:
                        line = line.replace('Îµ', 'ε')  # Reemplazar el simbolo Îµ por ε
                        if line.startswith("digraph"):
                            continue
                        if '->' in line:
                            parts = line.split('->')
                            from_node = parts[0].strip()
                            to_node = parts[1].split('[')[0].strip()
                            if from_node not in node_map:
                                new_from_node = f'{prefix}{node_offset}'
                                node_map[from_node] = new_from_node
                                if start_node is None:
                                    start_node = new_from_node
                                node_offset += 1
                            if to_node not in node_map:
                                new_to_node = f'{prefix}{node_offset}'
                                node_map[to_node] = new_to_node
                                node_offset += 1
                            new_line = line.replace(from_node, node_map[from_node]).replace(to_node, node_map[to_node])
                            edges.append(new_line)
                        elif '[' in line:
                            node = line.split('[')[0].strip()
                            if node not in node_map:
                                new_node = f'{prefix}{node_offset}'
                                node_map[node] = new_node
                                if start_node is None:
                                    start_node = new_node
                                node_offset += 1
                            new_line = line.replace(node, node_map[node])
                            edges.append(new_line)
                    return edges, node_offset, start_node

            node_offset = 1
            thompson_edges, node_offset, thompson_start = extract_and_rename_nodes(self.thompson_output, 'T', node_offset)
            subsets_edges, node_offset, subsets_start = extract_and_rename_nodes(self.subsets_output, 'S', node_offset)
            minimization_edges, node_offset, minimization_start = extract_and_rename_nodes(self.minimization_output, 'M', node_offset)

            # Anadir los nodos y aristas al grafo combinado sin usar subgrafos con etiquetas
            combined_graph.body.extend(thompson_edges)
            combined_graph.body.extend(subsets_edges)
            combined_graph.body.extend(minimization_edges)

            # Conectar nodos iniciales de los subgrafos al nodo principal
            combined_graph.edge('start', thompson_start)
            combined_graph.edge('start', subsets_start)
            combined_graph.edge('start', minimization_start)

            combined_graph.attr(rankdir='TB', size='10,10!')
            combined_graph.attr('node', shape='circle')

            combined_graph.render('combined_graph', format='png')
            self.log_message("Grafo combinado generado como 'combined_graph.png'")

            # Abrir el archivo .png generado
            os.startfile('combined_graph.png')

        except Exception as e:
            self.log_message(f"Error al combinar grafos: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LexicalAnalyzer(root)
    root.mainloop()