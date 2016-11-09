#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
# TODO: Permitir editar la definición

targetFile = '/home/david/Downloads/Anki Decks/ankiVocDeck.txt'


def pref(x):
    return {
        "sustantivo\n": "(n.) ",
        "verbo\n": "(v.) ",
        "adjetivo\n": "(adj.) ",
        "adverbio\n": "(adv.) ",
        "preposición\n": "(prep.) ",
        "exclamación\n": "(excl.)",
        "conjunción\n": "(conj.)"
    }.get(x, "")   # "" is default if x not found


os.system("xclip -o > .text")
f = open('.text', 'r')
concept = f.read().split()
if len(concept) == 1:
    definitions = ""
    os.system("trans -d en:en `cat .text` > .translation")

    f = open('.translation', 'r')
    concept = f.readline()
    concept = concept[:-1]
    concept = concept.lower()
    phonetic = f.readline()
    if phonetic[0] == '/':  # There was a phonetic line
        f.readline()  # Now there is an empty line then
    line = f.readline()
    prefix = pref(line)
    finish = prefix == ""
    line = f.readline().split()
    counter = 0
    while finish is not True:
        counter += 1
        line = line[1:len(line)]
        if len(line) == 0:
            break
        line[len(line) - 1] = line[len(line) - 1].split('.')[0]
        definitions += "FALSE \"\\\""
        definitions += prefix
        for word in line:
            definitions += word + " "
        line = f.readline()  # read example
        if line[0] == '"':
            definitions += "(e.g. "
            line = line[line.find("\"") + 1:]

            # remove concept variations
            dots = "....."
            line = line[: -1].replace(concept + "s", dots)
            line = line.replace(concept + "es", dots)
            if concept[-1] == 'e':
                line = line.replace(concept + "d", dots)
            line = line.replace(concept + "ed", dots)
            line = line.replace(concept + concept[-1:] + "ed", dots)
            line = line.replace(concept + "ing", dots)
            line = line.replace(concept + concept[-1:] + "ing", dots)
            if concept[-1:] == 'y':
                line = line[: -1].replace(concept[:-1] + "ies", dots)
            line = line[: -1].replace(concept, dots)

            definitions += line + ")"
        definitions += "\\\"; " + concept + "\" "
        line = f.readline()
        if line == "Sinónimos\n" or line == "Ejemplos\n" or line == "Ver también":
            finish = True
        while line != "\n":
            line = f.readline()
        line = f.readline()
        if line == "Sinónimos\n" or line == "Ejemplos\n" or line == "Ver también":
            finish = True
        else:
            new_prefix = pref(line)
            if new_prefix != "":
                prefix = new_prefix
                line = f.readline().split()
            else:
                line = line.split()
    if counter == 1:
        definitions = definitions.replace("\\\"", "\"")[7:-2]
        confirm = os.system("zenity --question --ok-label=\"Ok\" --cancel-label=\"Cancelar\"  --height=10 --text=\"" +
                            "Añadida a anki la tarjeta:\n" + definitions.replace("\"", "\\\"") + "\"")
        if confirm == 0:
            f = open(targetFile, 'a')
            f.write(definitions + "\n")
            f.close()
    elif counter > 1:
        os.system("ans=$(zenity  --list --text '" + concept + " - Seleciona las definiciones para añadir a la base de datos de Anki' --checklist  --column \"Pick\" --column \"Definitions\" " +
                  definitions + "  --width=500 --height=450); echo $ans > .answer")
        f.close()

        f = open('.answer', 'r')
        lines = f.read()
        lines = lines[:-1].split('|')
        f.close

        f = open(targetFile, 'a')
        for line in lines:
            f.write(line + "\n")
        f.close()
        os.system("rm .answer")
    else:  # no definitions found
        os.system("zenity --question --ok-label=\"Ok\" --cancel-label=\"Cancelar\"  --height=10 --text=\"No se ha encontrado una definición para \\\"" + concept + "\\\" \"")

    os.system("rm .text .translation")
