# anki_cards_generator
Python script that takes an english word from the clipboard and searches its different definitions, examples in sentences, kind of word (noun, verb...) in google translate using https://github.com/soimort/translate-shell/. It asks you to select the definitions you want to import to anki and for each of them, the program generates a line with the right format to import this word to http://ankisrs.net/ or Anki Desktop. The program appends these lines to a file you have previously selected. 

This script is licensed under MIT but note that in order to use it completely you need to install some dependencies. In particular https://github.com/soimort/translate-shell/ can just be used for private use.

#Install and setup
Install python, zenity, xclip and https://github.com/soimort/translate-shell/

Change the value of the variable targetFile to select the file where you want the definitions to be stored

#Screenshots
![alt tag](https://github.com/eticaasdf/anki_cards_generator/blob/master/una.png)
![alt tag](https://github.com/eticaasdf/anki_cards_generator/blob/master/dos.png)
