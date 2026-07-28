import json

from parser import parsear_registro


with open("SUAC1.JUNIO26", "r", encoding="latin1") as entrada, \
     open("SUAC1.JUNIO26.json", "w", encoding="utf-8") as salida:

    salida.write("[\n")

    primero = True

    for linea in entrada:
        registro = parsear_registro(linea)

        if not primero:
            salida.write(",\n")

        json.dump(registro, salida, ensure_ascii=False, default=float)

        primero = False

    salida.write("\n]")
