class Grammar:
    def __init__(self):
        self.productions = {
            'expression': [
                ('expression', 'PLUS', 'term'),
                ('expression', 'MINUS', 'term'),
                ('term',)
            ],
            'term': [
                ('term', 'MULT', 'factor'),
                ('term', 'DIV', 'factor'),
                ('factor',)
            ],
            'factor': [
                ('LPAREN', 'expression', 'RPAREN'),
                ('Identifier',),
                ('Number',)
            ]
        }
        self.tokens = {'Identifier', 'Number', 'PLUS', 'MINUS', 'MULT', 'DIV', 'LPAREN', 'RPAREN'}
        self.non_terminals = {'expression', 'term', 'factor', 'S'}  # Agregar el símbolo aumentado
        self.first_sets = {nt: set() for nt in self.non_terminals}  # Inicialización de FIRST sets
        self.follow_sets = {nt: set() for nt in self.non_terminals}  # Inicialización de FOLLOW sets
        self.start_symbol = 'expression'  # Símbolo de inicio original
        self.augmented_start = 'S'  # Un nuevo símbolo de inicio para la producción aumentada
        self.productions[self.augmented_start] = [(self.start_symbol,)]  # Producción aumentada

    def compute_first_sets(self):
                changed = True
                for non_terminal in self.non_terminals:
                    self.first_sets[non_terminal] = set()

                while changed:
                    changed = False
                    for head, productions in self.productions.items():
                        for production in productions:
                            # Calculate FIRST(production)
                            for symbol in production:
                                if symbol in self.tokens:  # If it's a terminal
                                    if symbol not in self.first_sets[head]:
                                        self.first_sets[head].add(symbol)
                                        changed = True
                                    break  # Stop at the first terminal
                                else:  # It's a non-terminal
                                    before = len(self.first_sets[head])
                                    self.first_sets[head].update(self.first_sets[symbol] - set([None]))
                                    if None in self.first_sets[symbol]:
                                        continue
                                    if len(self.first_sets[head]) != before:
                                        changed = True
                                    break
                            else:
                                self.first_sets[head].add(None)

    def compute_follow_sets(self):
        # Inicializar el conjunto FOLLOW de cada no terminal
        for non_terminal in self.non_terminals:
            self.follow_sets[non_terminal] = set()

        # El símbolo de inicio de la gramática debería tener el marcador de fin de entrada '$' en su conjunto FOLLOW
        self.follow_sets[self.start_symbol].add('$')

        # Repetir el proceso hasta que no haya más cambios en los conjuntos FOLLOW
        changed = True
        while changed:
            changed = False
            for head, productions in self.productions.items():
                for production in productions:
                    # Comenzar con FOLLOW del lado izquierdo de la producción
                    follow_temp = self.follow_sets[head].copy()

                    # Revisar cada símbolo de la producción de derecha a izquierda
                    for i in reversed(range(len(production))):
                        symbol = production[i]
                        if symbol in self.non_terminals:
                            # Actualizar el FOLLOW del símbolo con follow_temp
                            before = len(self.follow_sets[symbol])
                            self.follow_sets[symbol].update(follow_temp)
                            if len(self.follow_sets[symbol]) > before:
                                changed = True

                            # Si FIRST del símbolo contiene épsilon, se añade FOLLOW del símbolo al follow_temp
                            if None in self.first_sets[symbol]:
                                follow_temp.update(self.first_sets[symbol] - set([None]))
                            else:
                                # Si no contiene épsilon, se reemplaza follow_temp con FIRST del símbolo
                                follow_temp = self.first_sets[symbol].copy()
                        else:
                            # Para terminales, simplemente se reinicia el follow_temp
                            follow_temp = self.first_sets[symbol] if symbol in self.first_sets else set()

                    # Después del último símbolo, el follow_temp se asigna al FOLLOW del lado izquierdo de la producción
                    if len(production) > 0:
                        last_symbol = production[-1]
                        if last_symbol in self.non_terminals:
                            before = len(self.follow_sets[last_symbol])
                            self.follow_sets[last_symbol].update(follow_temp)
                            if len(self.follow_sets[last_symbol]) > before:
                                changed = True

# Example usage
grammar = Grammar()
grammar.compute_first_sets()
grammar.compute_follow_sets()
