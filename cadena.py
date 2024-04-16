import re

'''Lee el contenido completo de un archivo y devuelve la cadena'''
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

'''Verifica si la cadena completa coincide con la expresión regular'''
def match_regex(regex, string):
    pattern = re.compile(regex)
    match = pattern.fullmatch(string)
    return match is not None

def main():
    regex_path = 'infix.txt' 
    string_path = 'cadena.txt'
    
    regex = read_file(regex_path)
    string = read_file(string_path)
    
    result = match_regex(regex, string) #verificar si la cadena coincide con la expresión regular
    print("w ∈ L(r):", result)

if __name__ == '__main__':
    main()