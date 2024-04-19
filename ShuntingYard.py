'''Convierte una expresión regular de notación infija a postfija utilizando el algoritmo Shunting Yard.'''

def to_postfix(expression):
    precedence = {'*': 3, '?': 3, '+': 3, '•': 2, '|': 1, '(': 0}
    stack = []
    output = []
    i = 0
    while i < len(expression):
        token = expression[i]
        if token.isalnum() or token in ('.', '_', '\\'):  # Considerando caracteres y escapados como parte del output directo
            output.append(token)
        elif token == '[':  # Manejar clases de caracteres como un solo token
            start = i
            i += 1  # Avanza para capturar todo el contenido dentro de los corchetes
            while expression[i] != ']':
                i += 1
            output.append(expression[start:i + 1])  # Incluye el cierre de corchete
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Remover el '(' del stack
        elif token in precedence:
            while stack and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        i += 1

    while stack:
        output.append(stack.pop())  # Vaciar los restos del stack al output

    return ''.join(output)

def process_yalex_file(input_path, output_path):
    postfix_expressions = []
    with open(input_path, 'r') as file:
        for line in file:
            if ':=' in line:
                token_name, regex = line.split(':=')
                postfix_regex = to_postfix(regex.strip())
                postfix_expressions.append(f"{token_name.strip()} := {postfix_regex}")

    with open(output_path, 'w') as file:
        file.write('\n'.join(postfix_expressions))

# Ejemplo de cómo usar la función
process_yalex_file('hard.yalex', 'output_postfix.yalex')