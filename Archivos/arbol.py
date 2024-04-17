class Node:
    def __init__(self, char, position=None, nullable=False):
        self.char = char  #almacena el caracter del nodo
        self.position = position  #almacena la posicion del nodo en la expresion
        self.firstposition = set()  #conjunto de posiciones que pueden aparecer primero
        self.lastposition = set()  #conjunto de posiciones que pueden aparecer ultimo
        self.nextposition = {}  #diccionario de posiciones siguientes para cada posicion
        self.nullable = nullable  #indica si el nodo puede representar una cadena vacia
        self.leftnode = None  #nodo hijo izquierdo
        self.rightnode = None  #nodo hijo derecho

    def set_positions(self):
        if self.leftnode:  #si existe un nodo izquierdo
            self.leftnode.set_positions()  #calcula las posiciones para el subarbol izquierdo
        if self.rightnode:  #si existe un nodo derecho
            self.rightnode.set_positions()  #calcula las posiciones para el subarbol derecho

        if self.char == 'ε':  #si el caracter es epsilon
            self.nullable = True  #el nodo es nullable
        elif self.char.isalnum():  #si el caracter es alfanumerico
            self.firstposition = {self.position}  #la primera posicion es la del nodo
            self.lastposition = {self.position}  #la ultima posicion es la del nodo
            self.nullable = False  #el nodo no es nullable
        elif self.char == '|':  #si el caracter es union
            self.firstposition = self.leftnode.firstposition | self.rightnode.firstposition  #la primera posicion es la union de las primeras posiciones de los hijos
            self.lastposition = self.leftnode.lastposition | self.rightnode.lastposition  #la ultima posicion es la union de las ultimas posiciones de los hijos
            self.nullable = self.leftnode.nullable or self.rightnode.nullable  #es nullable si alguno de los hijos es nullable
        elif self.char == '•':  #si el caracter es una concatenacion (•)
            self.firstposition = self.leftnode.firstposition | (self.rightnode.firstposition if self.leftnode.nullable else set())  #la primera posicion depende de si el hijo izquierdo es nullable
            self.lastposition = self.rightnode.lastposition | (self.leftnode.lastposition if self.rightnode.nullable else set())  #la ultima posicion depende de si el hijo derecho es nullable
            self.nullable = self.leftnode.nullable and self.rightnode.nullable  #es nullable si ambos hijos son nullable
            for pos in self.leftnode.lastposition:  #para cada posicion en la ultima posicion del hijo izquierdo
                for next_pos in self.rightnode.firstposition:  #para cada posicion en la primera posicion del hijo derecho
                    if pos not in self.nextposition:
                        self.nextposition[pos] = set()  #crea un nuevo conjunto si no existe
                    self.nextposition[pos].add(next_pos)  #añade la posicion siguiente
        elif self.char == '*':  #si el caracter es un cierre de kleene
            self.firstposition = self.leftnode.firstposition  #la primera posicion es la del hijo
            self.lastposition = self.leftnode.lastposition  #la ultima posicion es la del hijo
            self.nullable = True  #siempre es nullable
            for pos in self.lastposition:  #para cada posicion en la ultima posicion
                if pos not in self.nextposition:
                    self.nextposition[pos] = set()  #crea un nuevo conjunto si no existe
                self.nextposition[pos].update(self.firstposition)  #actualiza con las primeras posiciones
        elif self.char == '+':  #si el caracter es un positivo
            self.firstposition = self.leftnode.firstposition  #la primera posicion es la del hijo
            self.lastposition = self.leftnode.lastposition #la ultima posicion es la del hijo
            self.nullable = False  #no es nullable
            for pos in self.lastposition: #para cada posicion en la ultima posicion
                if pos not in self.nextposition:
                    self.nextposition[pos] = set()  #crea un nuevo conjunto si no existe
                self.nextposition[pos].update(self.firstposition)  #actualiza con las primeras posiciones

    def print_tree(self, indent="", result=None):
        if result is None:  #si el resultado es None
            result = []  #inicializa la lista de resultado
        result.append(indent + self.char)  #añade el caracter del nodo a la lista con la indentacion
        if self.leftnode:  #si hay un nodo izquierdo
            self.leftnode.print_tree(indent + "  ", result)  #imprime el subarbol izquierdo con mas indentacion
        if self.rightnode:  #si hay un nodo derecho
            self.rightnode.print_tree(indent + "  ", result)  #imprime el subarbol derecho con mas indentacion
        return result  #retorna la lista de caracteres

operators = ["*", "|", "•", "+", "?"]  #lista de operadores

'''construccion de arbol sintactico'''
def build_tree(expression):
    build = []  #lista para construir el arbol
    expression = expression.replace(" ", "")  #elimina espacios de la expresion

    i = 0  #indice para asignar posiciones a caracteres alfanumericos

    for char in expression:  #para cada caracter en la expresion
        if char in operators:  #si el caracter es un operador
            if char in ('+', '*', '?'):  #si el operador es unario
                if not build:  #si la pila esta vacia
                    raise ValueError(f"Expresión postfix mal formada: no hay suficientes operandos para el operador '{char}'")
                node = build.pop()  #extrae el nodo de la pila
                op_node = Node(char)  #crea un nuevo nodo operador
                op_node.leftnode = node  #asigna el nodo extraido como hijo izquierdo
                build.append(op_node)  #añade el nodo operador a la pila
            elif char in ('|', '•'):  #si el operador es binario
                if len(build) < 2:  #si no hay suficientes nodos en la pila
                    raise ValueError(f"Expresión postfix mal formada: no hay suficientes operandos para el operador '{char}'")
                right_node = build.pop()  #extrae el nodo derecho
                left_node = build.pop()  #extrae el nodo izquierdo
                op_node = Node(char)  #crea un nuevo nodo operador
                op_node.leftnode = left_node  #asigna el nodo izquierdo
                op_node.rightnode = right_node  #asigna el nodo derecho
                build.append(op_node)  #añade el nodo operador a la pila
        else:  #si el caracter es un operando
            if char.isdigit() or char.isalpha() or char == 'ε':  #si es un digito, una letra o epsilon
                nullable = True if char == 'ε' else False  #determina si el nodo es nullable
                build.append(Node(char, i + 1, nullable))  #añade un nuevo nodo a la pila
                i += 1  #incrementa el indice
            else:  #si el caracter no es valido
                raise ValueError(f"Carácter '{char}' no es un operando válido")

    '''manejo de concatencion implicita al final de la expresion'''
    if len(build) == 2:  #si hay dos nodos en la pila
        right_node = build.pop()  #extrae el nodo derecho
        left_node = build.pop()  #extrae el nodo izquierdo
        dot_node = Node('•')  #crea un nodo de concatenacion
        dot_node.leftnode = left_node  #asigna el nodo izquierdo
        dot_node.rightnode = right_node  #asigna el nodo derecho
        build.append(dot_node)  #añade el nodo de concatenacion a la pila

    if len(build) != 1:  #si la pila final no contiene exactamente un elemento
        raise ValueError("La expresión postfix está mal formada: la pila final debe contener exactamente un elemento")
    return build[0]  #retorna el nodo raiz del arbol construido

def main():
    with open('postfix.txt', 'r') as file:
        postfix_expr = file.read().strip()
    
    root = build_tree(postfix_expr) #construir el arbol sintactico
    
    tree_representation = root.print_tree() #representación del arbol como lista de cadenas
    
    with open('arbol.txt', 'w') as file:
        file.write('\n'.join(tree_representation))

    #print("\nÁrbol de la expresión regular:")
    #print('\n'.join(tree_representation))

if __name__ == "__main__":
    main()