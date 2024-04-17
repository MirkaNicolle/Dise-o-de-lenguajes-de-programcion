'''Convierte una expresión regular de notación infija a postfija utilizando el algoritmo Shunting Yard.'''

def to_postfix(infix_expr):
    prec = {'(': 1, '|': 2, '•': 3, '?': 4, '*': 4, '+': 4, '^': 5}
    special_characters = {'[': ']', '(': ')'}  # Caracteres especiales y sus pares

    def add_concatenation_operators(expr):
        output = []
        prev_char = ''
        for char in expr:
            if prev_char and (prev_char.isalnum() or prev_char in ('*', '+', '?', ')', ']')) and (char.isalnum() or char in ('(', '[')):
                output.append("•")  # Agrega un operador de concatenación si es necesario
            if char == '\\' and prev_char != '\\':  # Evitar agregar el operador de concatenación después de un escape
                if output and output[-1] != '\\':
                    output.append(char)
                continue
            output.append(char)
            prev_char = char
        return ''.join(output)

    infix_expr = add_concatenation_operators(infix_expr)  # Procesa la entrada para manejar la concatenación implícita

    stack = []
    postfix_list = []
    i = 0

    while i < len(infix_expr):
        char = infix_expr[i]
        if char.isalnum() or char in ('.', ';', '"', '\\'):  # Agrega operandos directamente a la lista de postfix
            if char == '\\':  # Captura el caracter escapado como parte del operando
                postfix_list.append(infix_expr[i:i+2])
                i += 1
            else:
                postfix_list.append(char)
        elif char in special_characters:  # Trata los caracteres especiales como unidades
            start = i
            i += 1  # Salta el caracter actual
            while i < len(infix_expr) and infix_expr[i] != special_characters[char]:
                i += 1
            postfix_list.append(infix_expr[start:i + 1])  # Incluye el par en postfix
        elif char == '(':
            stack.append(char)
        elif char == ')':
            top_token = stack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = stack.pop()
        else:
            while stack and stack[-1] in prec and prec[stack[-1]] >= prec.get(char, 0):
                postfix_list.append(stack.pop())
            stack.append(char)
        i += 1

    while stack:
        postfix_list.append(stack.pop())  # Vacía la pila

    return ''.join(postfix_list)  # Devuelve la expresión en postfix

def process_yalex_file(input_path, output_path):
    """Lee un archivo YALex y escribe las expresiones en postfix a otro archivo."""
    postfix_expressions = []
    with open(input_path, 'r', encoding='utf-8') as file:  # Asegurarse de usar la codificación correcta
        for line in file:
            if ':=' in line:
                token_name, regex = line.split(':=')
                postfix_regex = to_postfix(regex.strip())
                postfix_expressions.append(f"{token_name.strip()} := {postfix_regex}")

    with open(output_path, 'w', encoding='utf-8') as file:  # Asegurarse de usar la codificación correcta
        file.write('\n'.join(postfix_expressions))

# Ejemplo de cómo usar la función
process_yalex_file('easy.yalex', 'output_postfix.txt')