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
            for item in state:
                if hasattr(item, 'is_final') and item.is_final():
                    if item.production.head == self.grammar.augmented_start:
                        slr_table[state_key]['$'] = 'Accept'
                    else:
                        for terminal in follow_sets[item.production.head]:
                            slr_table[state_key][terminal] = f'reduce {item.production}'
                else:
                    next_symbol = item.next_symbol() if hasattr(item, 'next_symbol') else None
                    if next_symbol in self.grammar.tokens:
                        next_state = self.automaton.goto(state, next_symbol)
                        next_state_key = frozenset(next_state)
                        slr_table[state_key][next_symbol] = f'shift {next_state_key}'
                    elif next_symbol in self.grammar.non_terminals:
                        next_state = self.automaton.goto(state, next_symbol)
                        next_state_key = frozenset(next_state)
                        slr_table[state_key][next_symbol] = next_state_key
        return slr_table

    def display_slr_table_as_text(self):
        result = ""
        action_columns = list(self.grammar.tokens) + ['$']
        goto_columns = list(self.grammar.non_terminals)
        states = list(self.slr_table.keys())

        for state in states:
            result += f"State: {state}\n"
            actions = self.slr_table[state]
            for symbol in action_columns + goto_columns:
                if symbol in actions:
                    result += f"  {symbol}: {actions[symbol]}\n"
            result += "\n"

        return result

    def save_slr_table_as_pdf(self, filepath='slr_table.pdf'):
        table_text = self.display_slr_table_as_text()
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        # Margins
        margin = 40
        textobject = c.beginText(margin, height - margin)
        textobject.setFont("Helvetica", 12)

        for line in table_text.split('\n'):
            if textobject.getY() < margin:
                c.drawText(textobject)
                c.showPage()
                textobject = c.beginText(margin, height - margin)
                textobject.setFont("Helvetica", 12)
            textobject.textLine(line)

        c.drawText(textobject)
        c.save()