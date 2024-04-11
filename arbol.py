class Node:
    def __init__(self, char, position=None, nullable=False):
        self.char = char
        self.position = position
        self.firstposition = set()
        self.lastposition = set()
        self.nextposition = set()
        self.nullable = nullable
        self.leftnode = None
        self.rightnode = None

    def set_positions(self):
        if self.leftnode:
            self.leftnode.set_positions()
        if self.rightnode:
            self.rightnode.set_positions()

        if self.char == 'ε':  # Manejo del carácter epsilon
            self.nullable = True
        elif self.char.isalnum():
            self.firstposition = {self.position}
            self.lastposition = {self.position}
            self.nullable = False
        elif self.char == '|':
            self.firstposition = self.leftnode.firstposition | self.rightnode.firstposition
            self.lastposition = self.leftnode.lastposition | self.rightnode.lastposition
            self.nullable = self.leftnode.nullable or self.rightnode.nullable
        elif self.char == '.':
            self.firstposition = self.leftnode.firstposition | (self.rightnode.firstposition if self.leftnode.nullable else set())
            self.lastposition = self.rightnode.lastposition | (self.leftnode.lastposition if self.rightnode.nullable else set())
            self.nullable = self.leftnode.nullable and self.rightnode.nullable
        elif self.char == '*':
            self.firstposition = self.leftnode.firstposition
            self.lastposition = self.leftnode.lastposition
            self.nullable = True

        # Set nextposition for child nodes
        if self.char == '•':
            for position in self.leftnode.lastposition:
                self.nextposition.update(self.rightnode.firstposition)
        elif self.char == '*':
            for position in self.lastposition:
                self.nextposition.update(self.firstposition)

    def print_tree(self, indent="", result=None):
        if result is None:
            result = []
        result.append(indent + self.char)
        if self.leftnode:
            self.leftnode.print_tree(indent + "  ", result)
        if self.rightnode:
            self.rightnode.print_tree(indent + "  ", result)
        return result

operators = ["*", "|", "•", "+", "?"]

def build_tree(expression):
    build = []
    expression = expression.replace(" ", "")

    i = 0  # Índice para asignar posiciones a caracteres alfanuméricos

    for char in expression:
        print(f"Carácter actual: {char}")
        print("Contenido de la pila build antes de procesar el carácter:")
        for node in build:
            print(f"  Nodo: {node.char}")
        print("-" * 20)

        if char in operators:
            if char in ('+', '*', '?'):
                if not build:
                    raise ValueError(f"Expresión postfix mal formada: no hay suficientes operandos para el operador '{char}'")
                node = build.pop()
                op_node = Node(char)
                op_node.leftnode = node
                build.append(op_node)
            elif char in ('|', '•'):
                if len(build) < 2:
                    raise ValueError(f"Expresión postfix mal formada: no hay suficientes operandos para el operador '{char}'")
                right_node = build.pop()
                left_node = build.pop()
                op_node = Node(char)
                op_node.leftnode = left_node
                op_node.rightnode = right_node
                build.append(op_node)
        else:
            # Aceptar dígitos y letras como operandos válidos
            if char.isdigit() or char.isalpha() or char == 'ε':
                nullable = True if char == 'ε' else False
                build.append(Node(char, i + 1, nullable))
                i += 1
            else:
                raise ValueError(f"Carácter '{char}' no es un operando válido")

    # Manejar la concatenación implícita al final de la expresión
    if len(build) == 2:
        right_node = build.pop()
        left_node = build.pop()
        dot_node = Node('•')
        dot_node.leftnode = left_node
        dot_node.rightnode = right_node
        build.append(dot_node)

    if len(build) != 1:
        raise ValueError("La expresión postfix está mal formada: la pila final debe contener exactamente un elemento")
    return build[0]

def main():
    # Leer la expresión regular en notación postfix desde el archivo generado por ShuntingYard.py
    with open('postfix.txt', 'r') as file:
        postfix_expr = file.read().strip()
    
    # Construir el árbol sintáctico
    root = build_tree(postfix_expr)
    
    # Obtener la representación del árbol como lista de cadenas
    tree_representation = root.print_tree()
    
    # Escribir la representación del árbol en un archivo
    with open('arbol.txt', 'w') as file:
        file.write('\n'.join(tree_representation))

    # Imprimir el árbol en la consola
    #print("\nÁrbol de la expresión regular:")
    #print('\n'.join(tree_representation))

if __name__ == "__main__":
    main()