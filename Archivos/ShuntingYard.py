'''Convierte una expresión regular de notación infija a postfija utilizando el algoritmo Shunting Yard.'''

def to_postfix(infix_expr):
    prec = {'(': 1, '|': 2, '•': 3, '?': 4, '*': 4, '+': 4, '^': 5} #diccionario con la precedencia de los operadores

    def add_concatenation_operators(expr): #agrega operadores de concatenación ('•') donde sea necesario
        output = []
        prev_char = ''
        for char in expr:
            if prev_char and ((prev_char.isalnum() or prev_char in ('*', '+', '?', ')')) and (char.isalnum() or char == '(')):
                output.append("•") #agrega un operador de concatenación si el carácter actual y el anterior requieren concatenación implícita
            output.append(char)
            prev_char = char
        return ''.join(output)

    infix_expr = add_concatenation_operators(infix_expr) #procesa la entrada para manejar la concatenación implícita

    stack = []  #pila para operadores
    postfix_list = []  #lista para guardar postfix

    for char in infix_expr:
        if char.isalnum() or char in ('.', ';', '"', '\\'): # Agrega operandos directamente a la lista de postfix
            postfix_list.append(char)
        elif char == '(':
            stack.append(char) #manejo de parantesis abiertos
        elif char == ')':
            top_token = stack.pop() #vacía la pila hasta el parantesis abierto mas cercano
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = stack.pop()
        else:
            while stack and prec[stack[-1]] >= prec[char]: #organizacion de operadores segun precedencia al actual
                postfix_list.append(stack.pop())
            stack.append(char)

    while stack:
        postfix_list.append(stack.pop())  #extraccion los operadores restantes

    return ''.join(postfix_list) #lista postfix

'''Creacion del archivo con expresion postfix'''

with open('infix.txt', 'r') as file: #archivo de entrada
    infix_exprs = file.readlines()

postfix_infix_exprs = []
for infix_expr in infix_exprs:
    postfix_infix_expr = to_postfix(infix_expr.strip()) #proceso linea por linea
    postfix_infix_exprs.append(postfix_infix_expr)

with open('postfix.txt', 'w') as file:
    file.write('\n'.join(postfix_infix_exprs))
