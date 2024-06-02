import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from automaton import LR0Automaton

class SLRTable:
    def __init__(self, grammar):
        self.grammar = grammar
        self.automaton = LR0Automaton(grammar)
        self.slr_table = self.construct_slr_table()

    def construct_slr_table(self):
        slr_table = {}
        follow_sets = self.grammar.follow_sets

        for state in self.automaton.states:
            state_key = frozenset(state)
            slr_table[state_key] = {}
            # print(f"Estado: {state_key}")  # Depuración: Imprimir estado
            for item in state:
                if item[2] == len(item[1]):  # Si el punto está al final de la producción
                    if item[0] == self.grammar.augmented_start:
                        slr_table[state_key]['$'] = 'Accept'
                    else:
                        for terminal in follow_sets[item[0]]:
                            slr_table[state_key][terminal] = f'reduce {item}'
                else:
                    next_symbol = item[1][item[2]]
                    next_state = self.automaton.goto(state, next_symbol)
                    if next_state:
                        next_state_key = frozenset(next_state)
                        # print(f"  Transición con símbolo {next_symbol} a {next_state_key}")  # Depuración: Imprimir transición
                        if next_symbol in self.grammar.terminals:
                            slr_table[state_key][next_symbol] = f'shift {next_state_key}'
                        elif next_symbol in self.grammar.non_terminals:
                            slr_table[state_key][next_symbol] = next_state_key
        return slr_table

    def display_slr_table_as_dataframe(self):
        rows = []
        action_columns = list(self.grammar.terminals) + ['$']
        goto_columns = list(self.grammar.non_terminals)
        states = list(self.slr_table.keys())

        for state in states:
            state_repr = str(state)
            actions = self.slr_table[state]
            for symbol in action_columns:
                if symbol in actions:
                    rows.append((state_repr, 'Acción', actions[symbol]))
            for non_terminal in goto_columns:
                if non_terminal in actions:
                    rows.append((state_repr, 'Goto', actions[non_terminal]))

        df = pd.DataFrame(rows, columns=['Estado', 'Tipo', 'Transición'])
        return df

    def save_slr_table_as_pdf(self, filepath='slr_table.pdf'):
        df = self.display_slr_table_as_dataframe()
        table_data = [df.columns.values.tolist()] + df.values.tolist()

        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        # Margins
        margin = 40
        textobject = c.beginText(margin, height - margin)
        textobject.setFont("Helvetica", 8)

        for row in table_data:
            line = ' | '.join(map(str, row))
            if textobject.getY() < margin:
                c.drawText(textobject)
                c.showPage()
                textobject = c.beginText(margin, height - margin)
                textobject.setFont("Helvetica", 8)
            textobject.textLine(line)

        c.drawText(textobject)
        c.save()