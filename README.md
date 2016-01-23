# anki_cards_generator
Script de python que coge una palabra inglesa que has debido copiar al portapapeles y busca automáticamente la definición, ejemplos tipo de palabra etc en google translate, usando https://github.com/soimort/translate-shell/ y te genera una línea con el formato para importar a http://ankisrs.net/ y le hace append a un fichero que has elegido previamente. Si hay varias definiciones te muestra todas y te pide seleccionar unas cuantas.

Este archivo está bajo licencia MIT pero ten en cuenta que para usarlo en su completitud necesitas instalar algunas dependencias. En concreto https://github.com/soimort/translate-shell/ no se puede usar más que para uso particular.

#Instalación y puesta en marcha
Instala python, zenity, xclip y https://github.com/soimort/translate-shell/

Añade el valor de targetFile para seleccionar el archivo donde quieres que se guarden las definiciones.

#Capturas de pantalla
![alt tag](https://github.com/eticaasdf/anki_cards_generator/blob/master/una.png)
![alt tag](https://github.com/eticaasdf/anki_cards_generator/blob/master/dos.png)
