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
        self.non_terminals = {'expression', 'term', 'factor'}
        self.start_symbol = 'expression'  
        self.augmented_start = 'S'  
        self.first_sets = {nt: set() for nt in self.non_terminals}
        self.follow_sets = {nt: set() for nt in self.non_terminals}

    def primero_sets(self):
        # inicializa un indicador para determinar si el conjunto FIRST ha cambiado
        changed = True
        while changed:
            # asume que no hay cambios hasta encontrar uno
            changed = False
            # recorre todas las cabezas de produccion y sus producciones
            for head, productions in self.productions.items():
                for production in productions:
                    # analiza cada simbolo de la produccion
                    for symbol in production:
                        # si el simbolo es terminal y no esta en el conjunto FIRST del encabezado
                        if symbol in self.tokens:
                            if symbol not in self.first_sets[head]:
                                # añade el simbolo al conjunto FIRST del encabezado y marca que hubo un cambio
                                self.first_sets[head].add(symbol)
                                changed = True
                            # termina el bucle despues de encontrar el primer terminal
                            break
                        # si el simbolo es no terminal
                        elif symbol in self.first_sets:
                            # guarda el tamaño actual del conjunto FIRST para comparar despues de la actualizacion
                            before_change = len(self.first_sets[head])
                            # actualiza el conjunto FIRST del encabezado con los elementos del conjunto FIRST del simbolo
                            self.first_sets[head].update(self.first_sets[symbol] - {None})
                            # si el conjunto FIRST del simbolo contiene None, continúa al siguiente simbolo
                            if None in self.first_sets[symbol]:
                                continue
                            # si el tamaño del conjunto FIRST cambió, actualiza el indicador de cambio
                            if len(self.first_sets[head]) > before_change:
                                changed = True
                            # termina el bucle si no se necesita añadir None
                            break
                        # si el simbolo es el ultimo de la produccion, añade None al conjunto FIRST
                        if symbol == production[-1]:
                            self.first_sets[head].add(None)

    def siguiente_sets(self):
        # inicializa el conjunto FOLLOW para cada no terminal
        for non_terminal in self.non_terminals:
            self.follow_sets[non_terminal] = set()
        # añade el simbolo de finalizacion a el conjunto FOLLOW del simbolo de inicio
        self.follow_sets[self.start_symbol].add('$')

        # inicializa un indicador para determinar si el conjunto FOLLOW ha cambiado
        changed = True
        while changed:
            # asume que no hay cambios hasta encontrar uno
            changed = False
            # recorre todas las cabezas de produccion y sus producciones
            for head, productions in self.productions.items():
                for production in productions:
                    # empieza con el conjunto FOLLOW del encabezado de la produccion
                    follow_temp = self.follow_sets[head].copy()

                    # revisa cada simbolo de la produccion de derecha a izquierda
                    for i in reversed(range(len(production))):
                        symbol = production[i]
                        if symbol in self.non_terminals:
                            # actualiza el conjunto FOLLOW del simbolo con follow_temp
                            before_change = len(self.follow_sets[symbol])
                            self.follow_sets[symbol].update(follow_temp)
                            # si el conjunto FIRST del simbolo contiene None, actualiza follow_temp
                            if None in self.first_sets[symbol]:
                                follow_temp.update(self.first_sets[symbol] - {None})
                            else:
                                # si no contiene None, reemplaza follow_temp con el conjunto FIRST del simbolo
                                follow_temp = self.first_sets[symbol]
                            # si el conjunto FOLLOW del simbolo ha cambiado, marca que hubo un cambio
                            if len(self.follow_sets[symbol]) > before_change:
                                changed = True
                        else:
                            # para los terminales, reinicia follow_temp con el conjunto FIRST del simbolo, si existe
                            follow_temp = self.first_sets[symbol] if symbol in self.first_sets else set()

# Using the Grammar
grammar = Grammar()
grammar.primero_sets()
grammar.siguiente_sets()