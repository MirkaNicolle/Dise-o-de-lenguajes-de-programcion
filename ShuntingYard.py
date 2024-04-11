'''Convierte una expresión regular de notación infija a postfija utilizando el algoritmo Shunting Yard.
Mejorado para manejar automáticamente la concatenación implícita e incluye una gama más amplia de operadores'''

def to_postfix(infix_expr):

    # Precedencia de operadores
    prec = {'(': 1, '|': 2, '•': 3, '?': 4, '*': 4, '+': 4, '^': 5}

    # Función para agregar operadores de concatenación explícitos ('.') donde sea necesario
    def add_concatenation_operators(expr):
        output = []
        prev_char = ''
        for char in expr:
            if prev_char and ((prev_char.isalnum() or prev_char in ('*', '+', '?', ')')) and (char.isalnum() or char == '(')):
                output.append("•")
            output.append(char)
            prev_char = char
        return ''.join(output)


    infix_expr = add_concatenation_operators(infix_expr)  # Manejar la concatenación implícita

    stack = []  # Pila para almacenar operadores
    postfix_list = []  # Lista para almacenar la expresión en notación postfija

    # Iterar sobre cada carácter de la expresión
    for char in infix_expr:
        # Si el carácter es un operando o un símbolo permitido, agregarlo directamente a la salida
        if char.isalnum() or char in ('.', ';', '"', '\\'):
            postfix_list.append(char)
        # Si el carácter es un paréntesis abierto, apilarlo
        elif char == '(':
            stack.append(char)
        # Si es un paréntesis cerrado, desapilar hasta encontrar el paréntesis abierto correspondiente
        elif char == ')':
            top_token = stack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = stack.pop()
        else:
            # Mientras haya operadores en la pila con mayor o igual precedencia, desapilarlos a la salida
            while (stack) and (prec[stack[-1]] >= prec[char]):
                postfix_list.append(stack.pop())
            # Apilar el operador actual
            stack.append(char)

    # Desapilar cualquier operador restante en la pila
    while stack:
        postfix_list.append(stack.pop())

    # Retornar la expresión en notación postfija como cadena
    return ''.join(postfix_list)


'''
Creacion del archivo con expresion postfix
'''

with open('infix.txt', 'r') as file:
    infix_exprs = file.readlines()

postfix_infix_exprs = []
for infix_expr in infix_exprs:
    postfix_infix_expr = to_postfix(infix_expr.strip())
    postfix_infix_exprs.append(postfix_infix_expr)

with open('postfix.txt', 'w') as file:
    file.write('\n'.join(postfix_infix_exprs))