#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import clipboard

# TODO: Permitir editar la definición
# Sudo pip3 install clipboard


class AnkiAutomatic:

    target_file = '/home/david/Downloads/Anki Decks/ankiVocDeck.txt'
    last = ["Sinónimos", "Ejemplos", "Ver también"]

    def run(self):
        concept = clipboard.paste().strip()
        if concept.find(" ") != -1:
            return
        definitions = ""
        translation = os.popen("trans -d en:en " + concept).read()
        tr = ParseTranslation(translation)
        concept = tr.get_concept()
        prefix = self.pref(tr.next_line())
        if prefix == "":
            return
        line = self.normalize(tr.next_line())
        n_def = 0  # Number of definitions
        while True:
            n_def += 1
            if len(line) == 0:
                break
            # There must be a FALSE before every definition if there is more than one
            definitions += "FALSE \"\\\""
            definitions += prefix
            definitions += line
            definitions += self.parse_example(tr.next_line(), concept)
            definitions += "\\\"; " + concept + "\" "
            line = tr.next_line()
            if line in AnkiAutomatic.last:
                break
            if self.pref(line) == "":
                while line != "":
                    line = tr.next_line()
                line = tr.next_line()
                if line in AnkiAutomatic.last:
                    break
            new_prefix = self.pref(line)
            if new_prefix != "":  # Change of prefix
                prefix = new_prefix
                line = self.normalize(tr.next_line())
            else:
                line = self.normalize(line)
        card_lines = self.ask_user(n_def, definitions, concept)
        self.send_to_file(card_lines)

    def pref(self, x):
        return {
            "sustantivo": "(n.) ",
            "verbo": "(v.) ",
            "adjetivo": "(adj.) ",
            "adverbio": "(adv.) ",
            "preposición": "(prep.) ",
            "exclamación": "(excl.) ",
            "conjunción": "(conj.) "
        }.get(x, "")   # "" is default if x not found

    def normalize(self, line):
        # Remove first and last "words" which are format tags
        return line.rsplit('.', 1)[0].split(' ', 1)[1].strip()

    def parse_example(self, example, concept):
        if example[:11] == '        - \"':   # If there is example
            # This removes the concept or variations of it
            example = example.split("\"")[1]

            # remove concept variations
            dots = "....."
            example = example.replace(concept + "s", dots)
            example = example.replace(concept + "es", dots)
            if concept[-1] == 'e':
                example = example.replace(concept + "d", dots)
                example = example.replace(concept[:-1] + "ing", dots)
            example = example.replace(concept + "ed", dots)
            example = example.replace(concept + concept[-1] + "ed", dots)
            example = example.replace(concept + "ing", dots)
            example = example.replace(concept + concept[-1] + "ing", dots)
            if concept[-1] == 'y':
                example = example.replace(concept[:-1] + "ies", dots)
            example = example.replace(concept, dots)
            return " (e.g. " + example + ")"
        else:
            return ''

    def send_to_file(self, card_lines):
        f = open(AnkiAutomatic.target_file, 'a')
        for line in card_lines:
            f.write(line + "\n")
        f.close()

    def ask_user(self, n_def, definitions, concept):
        card_lines = []
        if n_def == 1:
            definitions = definitions.replace("\\\"", "\"")[7:-2]
            confirm = os.system('''zenity --question --ok-label=\"Ok\" --cancel-label=\"Cancelar\"  --height=10 --text=\" Se añadirá a anki la tarjeta:\n {} \"'''
                    .format(definitions.replace("\"", "\\\"")))
            if confirm == 0:
                card_lines.append(definitions)
        elif n_def > 1:
            lines = os.popen("zenity  --list --text '{} - Seleciona las definiciones para añadir a la base de datos de Anki' --checklist --column \"Pick\" --column \"Definitions\" {} --width=1000 --height=450".format(concept, definitions)).read()
            card_lines = lines[:-1].split('|')
        else:  # no definitions found
            os.system("zenity --question --ok-label=\"Ok\" --cancel-label=\"Cancelar\"  --height=10 --text=\"No se ha encontrado una definición para \\\"{}\\\" \"".format(concept))
        return card_lines


class ParseTranslation:

    def __init__(self, translation):
        self.translation = translation.split('\n')
        self.counter = -1
        self.concept = self.next_line().lower()
        phonetic = self.next_line()
        # If there was a phonetic line, extra read
        if len(phonetic) > 0 and phonetic[0] == '/':
            self.next_line()

    def next_line(self):
        self.counter += 1
        try:
            return self.translation[self.counter]
        except IndexError:
            return ''

    def get_concept(self):
        return self.concept


if __name__ == "__main__":
    AnkiAutomatic().run()
