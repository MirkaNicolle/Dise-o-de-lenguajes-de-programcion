class Node:
    def __init__(self, char, position=None, nullable=None):
        self.char = char
        self.position = position
        self.firstposition = {position}
        self.lastposition = {position}
        self.nextposition = set()
        self.nullable = nullable
        self.leftnode = None
        self.rightnode = None

    def setPositions(self):
        if self.rightnode:
            self.rightnode.setPositions()
        if self.leftnode:
            self.leftnode.setPositions()
        # Aquí van los pasos de Carlos
        if self.char == ".":
            self.leftnode.setPositions()

    def print_tree(self, indent=""):
        print(indent + self.char)
        if self.leftnode:
            self.leftnode.print_tree(indent + "  ")
        if self.rightnode:
            self.rightnode.print_tree(indent + "  ")

operators = ["*", "|", "."]

def build_tree(expression):
    build = []
    expression = expression.replace(" ","")

    i = 0

    for char in expression:
        if char in operators:
            if char == "*" :
                leftnode = build.pop()
                build.append(Node(char))
                build[-1].leftnode = leftnode
            else:
                rightnode = build.pop()
                leftnode = build.pop()
                build.append(Node(char))
                build[-1].leftnode = leftnode
                build[-1].rightnode = rightnode
        else:
            build.append(Node(char, i+1, False)) #aqui va if char = epsilon: nullable = true else nullable = false
        i += 1

    return build[0] 

def add_concatenation_dot(regex):
    result = []  # Lista para almacenar la nueva expresión con puntos de concatenación
    special_chars = {'|', '*', '(', ')'}  # Caracteres especiales en regex

    for i in range(len(regex) - 1):
        result.append(regex[i])
        # Casos donde se necesita añadir un punto '.'
        if (regex[i] not in special_chars and regex[i + 1] not in special_chars) or \
            (regex[i] not in special_chars and regex[i + 1] == '(') or \
            (regex[i] == ')' and regex[i + 1] not in special_chars) or \
            (regex[i] == '*' and regex[i + 1] not in special_chars) or \
            (regex[i] == '*' and regex[i + 1] == '('):
            result.append('.')

    result.append(regex[-1])  # Añadir el último carácter de la expresión regular
    return ''.join(result)

def shunting_yard(infix_expression):
    parsed_expresion = add_concatenation_dot(infix_expression)
    queue = []
    stack = []

    def get_precende(c):
        if char == "*" : return 3 #cerradura de kleene
        if char == "." : return 2 #union (ab)
        if char == "|" : return 1 #concatenacion (a y b)
        return 0

    i=0
    for char in parsed_expresion:
        if char.isalnum():
            queue.append(char)
        elif char in operators:
            while (stack and stack[-1] in operators and get_precende(stack[-1]) >= get_precende(char)):
                c = stack.pop()
                queue.append(c)
            stack.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                c=stack.pop()
                queue.append(c)
            c= stack.pop()
        i+=1

    while stack:
        c=stack.pop()
        queue.append(c)
    
    result = ""

    for c in queue:
        result += c
    return result

def main():
    # Función principal que solicita la expresión regular y la cadena de entrada, y realiza la simulación y minimización de autómatas
    regex = input("Ingrese la expresión regular en notación infix: ")
    input_string = input("Ingrese la cadena a validar: ")

    postfix_expression = shunting_yard(regex)
    #print(f"\nExpresión regular en notación postfix: {' '.join(postfix_expression)}")

    root = build_tree(postfix_expression)
    print("\nÁrbol de la expresión regular:")
    root.print_tree()

if __name__ == "__main__":
    main()