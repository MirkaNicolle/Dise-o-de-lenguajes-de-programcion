from generador_lexico import read_yalex_file, generate_lexical_analyzer_code

def main():
    file_path_yalex = 'hard_especificaciones.yalex'  # Asegúrate de que la ruta al archivo YALex sea correcta
    rules = read_yalex_file(file_path_yalex)  # Carga las definiciones de tokens

    # Especifica un nombre de archivo de salida para el código del analizador léxico generado
    output_file = 'lexical_analyzer.py'
    generate_lexical_analyzer_code(rules, output_file)

if __name__ == "__main__":
    main()