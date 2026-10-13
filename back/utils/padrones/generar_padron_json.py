import json
import sys
from tempfile import NamedTemporaryFile
from pathlib import Path

if __package__:
    from .parsear import parsear_registro
    from .prefijos import PREFIJOS
else:
    from parsear import parsear_registro
    from prefijos import PREFIJOS

#Localiza las carpetas de entrada y salida
# Raíz del proyecto: .../back/utils/padrones/descargarPadrones.py -> 3 niveles arriba. __file__ reperesenta el archivo del script, desde su ubicacion sube hasta la raiz del repo y costruye las rutas
RAIZ_DATOS = Path(__file__).resolve().parents[3]
BASE = RAIZ_DATOS / "datos" / "fuentes"
DESTINO = RAIZ_DATOS / "datos" / "fuentes_formateadas"

def validar_archivos(periodo: str, base: Path) -> list[Path]:
    if not periodo or not periodo.isalnum():
        raise ValueError("El período debe contener solamente letras y números.")

    archivos = [base / f"{prefijo}.{periodo}" for prefijo in PREFIJOS]
    faltantes = [archivo.name for archivo in archivos if not archivo.is_file()]
    if faltantes:
        raise ValueError(f"Faltan archivos obligatorios: {', '.join(faltantes)}")

    inesperados = [ #guarda los archivos que no estan especificados en la constante PREFIJOS. Los archivos demás.
        str(archivo.relative_to(base))
        for archivo in base.rglob("*")
        if archivo.is_file() and archivo not in archivos
    ]
    if inesperados:
        raise ValueError(f"Archivos inesperados: {', '.join(inesperados)}")

    return archivos


def generar_padron_json(periodo: str, base: Path = BASE, destino: Path = DESTINO) -> Path:
    periodo = periodo.upper()
    archivos = validar_archivos(periodo, base)
    registros = []

    for archivo in archivos:
        with archivo.open("r", encoding="latin1") as entrada:
            cantidad = 0
            for numero_linea, linea in enumerate(entrada, start=1):
                try:
                    registro = parsear_registro(linea)
                except ValueError as e:
                    raise ValueError(f"{archivo.name}, línea {numero_linea}: {e}") from e

                # Campos que no vienen del layout COBOL
                registro["tipo_archivo"] = archivo.stem
                registro["periodo"] = periodo
                registro["bloqueo"] = False
                registro["empresa"] = "DPI" #si no es necesario, lo podria removera este campo o ponerlo como vacio.
                registro["login"] = "ppaez" #este campo deberia ser de quien cargó. Ya que si se ve login como campos en modelos que no son Usuario, entonces se usa como quien hizo esa accion
                registro["activo"] = True

                # Campos del modelo que faltaban (se cargan al dar de baja un registro)
                registro["motivo"] = None
                registro["fecha_baja"] = None
                registros.append(registro)
                cantidad += 1

            if cantidad == 0:
                raise ValueError(f"El archivo {archivo.name} está vacío.")

    destino.mkdir(parents=True, exist_ok=True)
    salida = destino / f"{periodo}.json"
    temporal = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", dir=destino, delete=False) as f:
            temporal = Path(f.name)
            json.dump(registros, f, ensure_ascii=False, indent=4, default=float)
        temporal.replace(salida)
    finally:
        if temporal is not None:
            temporal.unlink(missing_ok=True)

    print(f"Generado: {salida} ({len(registros)} registros)")
    return salida


def main():
    if len(sys.argv) != 2:
        print("Uso: python generar_padron_json.py PERIODO", file=sys.stderr)
        return 1
    try:
        generar_padron_json(sys.argv[1])
    except (ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
