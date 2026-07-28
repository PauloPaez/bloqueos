import json

from pathlib import Path

from parsear import parsear_registro

raiz_repositorio = Path(__file__).resolve().parents[1]
directorio_fuentes = raiz_repositorio / "fuente_de_verdad"

for archivo in directorio_fuentes.rglob("*.*"):

    if not archivo.is_file():
        continue

    nombre_archivo = archivo.stem
    periodo = archivo.suffix.lstrip(".")

    with archivo.open("r", encoding="latin1") as entrada, \
         archivo.with_suffix(".json").open("w", encoding="utf-8") as salida:

        salida.write("[\n")

        primero = True

        for linea in entrada:
            registro = parsear_registro(linea)

            registro["TIPO_ARCHIVO"] = nombre_archivo
            registro["PERIODO"] = periodo

            if not primero:
                salida.write(",\n")

            json.dump(registro, salida, ensure_ascii=False, default=float)

            primero = False

        salida.write("\n]")

    print(f"Generado: {archivo.with_suffix('.json')}")
