def validar(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    in_tokens_section = False
    in_productions_section = False
    tokens_found = False
    ignore_found = False
    productions_found = False

    for line in lines:
        line = line.strip()

        # Verificar comentarios
        if line.startswith('/*') and line.endswith('*/'):
            continue

        # Verificar sección de TOKENS
        if line.startswith('%token'):
            in_tokens_section = True
            tokens_found = True
            continue

        if line.startswith('IGNORE'):
            ignore_found = True
            continue

        if line == '%%':
            in_tokens_section = False
            in_productions_section = True
            continue

        if in_productions_section and line.endswith(';'):
            productions_found = True
            continue

    if not tokens_found:
        return "No se encontraron tokens definidos correctamente."
    if not ignore_found:
        return "No se encontraron tokens ignorados correctamente definidos."
    if not productions_found:
        return "No se encontraron producciones definidas correctamente."
    return "La gramática es válida según las consideraciones."

