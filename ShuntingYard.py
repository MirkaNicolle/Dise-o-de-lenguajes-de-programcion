'''Convierte una expresión regular de notación infija a postfija utilizando el algoritmo Shunting Yard.'''

def to_postfix(expression):
    precedence = {'*': 3, '?': 3, '+': 3, '•': 2, '|': 1, '(': 0}  #precedencia
    stack = []  #pila para almacenar operadores
    output = []  #salida en formato postfix
    i = 0  #iterar sobre la expresion
    while i < len(expression):  #mientras queden caracteres por procesar
        token = expression[i]  #obtiene el caracter actual
        if token.isalnum() or token in ('.', '_', '\\'):  #si es alfanumerico o alguno de estos simbolos
            if expression[i:i+2] in ('\\+', '\\s'):  # Manejar casos especiales de caracteres escapados
                output.append(expression[i:i+2])
                i += 2  # Avanzar un extra para saltar el caracter escapado
                continue
            else:
                output.append(token)  # o añade directamente al output
        elif token == '[':  #inicio de una clase de caracteres
            start = i  #guarda la posicion inicial del corchete
            i += 1  #avanza para incluir el contenido entre corchetes
            while expression[i] != ']':  #hasta encontrar el cierre de corchetes
                i += 1
            output.append(expression[start:i + 1])  #añade toda la clase de caracteres como un token al output
        elif token == '(':  #si encuentra un parentesis abierto
            stack.append(token)  #lo añade a la pila
        elif token == ')':  #si encuentra un parentesis cerrado
            while stack and stack[-1] != '(':  #vacia la pila hasta encontrar un parentesis abierto
                output.append(stack.pop())  
            stack.pop()  #elimina el parentesis abierto de la pila
        elif token in precedence:  #si el token es un operador
            while stack and precedence[stack[-1]] >= precedence[token]:  #mientras la pila no este vacia y el operador en la cima tenga mayor o igual precedencia
                output.append(stack.pop())  #añade el operador de la pila al output
            stack.append(token)  #añade el operador actual a la pila
        i += 1  #avanza al siguiente caracter

    while stack:  # vaciar operadores restantes en la pila
        output.append(stack.pop())  

    return ''.join(output)  #convierte la lista de output en una cadena y la retorna

def process_yalex_file(input_path, output_path):
    postfix_expressions = []  # lista para guardar las expresiones en postfix
    with open(input_path, 'r') as file:  
        for line in file:  # para cada linea en el archivo
            if ':=' in line:  #si la linea contiene una definicion de token
                token_name, regex = line.split(':=')  #separa el nombre del token y la expresion regular
                postfix_regex = to_postfix(regex.strip())  #convierte la regex a postfix
                postfix_expressions.append(f"{token_name.strip()} := {postfix_regex}")  #guarda la expresion en formato token_name := expresion_postfix

    with open(output_path, 'w') as file: 
        file.write('\n'.join(postfix_expressions)) 

process_yalex_file('easy.yalex', 'output_postfix.yalex')