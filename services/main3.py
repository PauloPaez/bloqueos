import json

from pathlib import Path

from parsear import parsear_registro


BASE = Path("../fuente_de_verdad")
DESTINO = Path("../padrones")

DESTINO.mkdir(exist_ok=True)

registros = []
periodo = None

for archivo in BASE.rglob("*.*"):

    if not archivo.is_file():
        continue

    nombre_archivo = archivo.stem

    if periodo is None:
        periodo = archivo.suffix.lstrip(".")

    with archivo.open("r", encoding="latin1") as entrada:

        for linea in entrada:

            registro = parsear_registro(linea)

            registro["tipo_archivo"] = nombre_archivo
            registro["periodo"] = periodo
            registro["bloqueo"] = False
            registro["empresa"] = "DPI"
            registro["login"] = "ppaez"
            registro["activo"] = True

            registros.append(registro)

salida = DESTINO / f"{periodo}.json"

with salida.open("w", encoding="utf-8") as f:
    json.dump(registros, f, ensure_ascii=False, indent=4, default=float)

print(f"Generado: {salida}")
