'''
Conversión de una expresión regular en notación infix a notación postfix basado en algoritmo Shunting Yard
'''
def to_postfix(infix_expr): #shuting yard
    prec = {'(': 1,
            '|': 2, 
            '.': 3, 
            '?': 4, 
            '*': 4, 
            '+': 4, 
            '^': 5,
            '/': 6,
            '-': 6}

    stack = []
    postfix_list = []

    for char in infix_expr:
        if char.isalnum() or char in ('.', ';', '"'):
            postfix_list.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack[-1] != '(':
                postfix_list.append(stack.pop())
            stack.pop() 
        else:
            while stack and stack[-1] != '(' and prec[char] <= prec[stack[-1]]:
                postfix_list.append(stack.pop())
            stack.append(char)

    while stack:
        postfix_list.append(stack.pop())

    return ''.join(postfix_list)

'''
Creacion del archivo con expresion postfix
'''

with open('expresion.txt', 'r') as file:
    infix_exprs = file.readlines()

postfix_infix_exprs = []
for infix_expr in infix_exprs:
    postfix_infix_expr = to_postfix(infix_expr.strip())
    postfix_infix_exprs.append(postfix_infix_expr)

with open('postfix.txt', 'w') as file:
    file.write('\n'.join(postfix_infix_exprs))