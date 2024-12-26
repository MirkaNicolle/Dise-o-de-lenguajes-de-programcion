# Diseño de lenguajes de programacion
### Mirka Monzon 18139
### puthon 3.11

Para este laborotario se espera realizar un analizador lexico funcional con todos los requerimientos solicitados, para mas informacion ver las instrucciones dentro del folder Instrucciones

Ejemplo de resultado (**test.py**):

Testing input: variable1 = 123 * (inputValue / 12)
Expected tokens: Numbers, operators, and identifiers
Tokens found: [('VARIABLE', 'Identifier'), (1, 'Number'), ('=', 'Operator'), (123, 'Number'), ('*', 'Operator'), ('(', 'Operator'), ('INPUTVALUE', 'Identifier'), ('/', 'Operator'), (12, 'Number'), (')', 'Operator')]

Testing input: // Comentario simple que debería ser ignorado
Expected token: Identifier
Tokens found: [('/', 'Operator'), ('/', 'Operator'), ('COMENTARIO', 'Identifier'), ('SIMPLE', 'Identifier'), ('QUE', 'Identifier'), ('DEBERÍA', 'Identifier'), ('SER', 'Identifier'), ('IGNORADO', 'Identifier')]

Testing input: if (x > 10) { return x; }
Complex test with conditions and blocks
Tokens found: [('IF', 'Identifier'), ('(', 'Operator'), ('X', 'Identifier'), ('>', 'Operator'), (10, 'Number'), (')', 'Operator'), ('{', 'Operator'), ('RETURN', 'Identifier'), ('X', 'Identifier'), (';', 'Operator'), ('}', 'Operator')]

Testing input: alpha123 = beta456 + gamma789
Expected error: Invalid identifier
Tokens found: [('ALPHA', 'Identifier'), (123, 'Number'), ('=', 'Operator'), ('BETA', 'Identifier'), (456, 'Number'), ('+', 'Operator'), ('GAMMA', 'Identifier'), (789, 'Number')]

Testing input: /* This is a comment */
Expected: Comments to be ignored
Tokens found: [('/', 'Operator'), ('*', 'Operator'), ('THIS', 'Identifier'), ('IS', 'Identifier'), ('A', 'Identifier'), ('COMMENT', 'Identifier'), ('*', 'Operator'), ('/', 'Operator')]

Testing input: "string with spaces"
Expected token: String with spaces
Tokens found: [('string with spaces', 'String')]

Testing input: 5.67
Expected token: Floating point number
Tokens found: [(5, 'Number'), ('.', 'Operator'), (67, 'Number')]

![image](https://github.com/MirkaNicolle/Dise-o-de-lenguajes-de-programcion/assets/35476538/77406427-2195-4735-87e9-794bb0e56eb6)
