import re

def read_file(file_path):
    """Lee el contenido completo de un archivo y devuelve la cadena."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def match_regex(regex, string):
    """Verifica si la cadena completa coincide con la expresión regular."""
    pattern = re.compile(regex)
    match = pattern.fullmatch(string)
    return match is not None

def main():
    regex_path = 'infix.txt'  # Nombre del archivo que contiene la expresión regular
    string_path = 'cadena.txt'  # Nombre del archivo que contiene la cadena a comprobar
    
    # Leer los contenidos de los archivos
    regex = read_file(regex_path)
    string = read_file(string_path)
    
    # Verificar si la cadena coincide con la expresión regular
    result = match_regex(regex, string)
    print("w ∈ L(r):", result)

if __name__ == '__main__':
    main()