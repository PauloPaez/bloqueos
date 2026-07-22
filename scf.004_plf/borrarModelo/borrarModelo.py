from pathlib import Path
import sys

# Nombre de la clase a generar
nombre_clase = sys.argv[1].lower()

def borrarArchivo(archivo):

    if archivo.exists():
        try:
            archivo.unlink()  # Eliminar el archivo
            print(f"Archivo '{archivo}' eliminado correctamente.")
        except Exception as e:
            print(f"Error al intentar eliminar el archivo '{archivo}': {e}")
        else:
            print(f"El archivo '{archivo}' no existe.")
    
    
# Ruta actual
directorio_actual = Path(__file__).resolve().parent

# Ruta back/models/XXX
archivo_para_borrar = directorio_actual.parent.parent / "back" / "models" / f"{nombre_clase}.py"
borrarArchivo(archivo_para_borrar)

# Ruta back/schemas/XXX
archivo_para_borrar = directorio_actual.parent.parent / "back" / "schemas" / f"{nombre_clase}.py"
borrarArchivo(archivo_para_borrar)

# Ruta back/querys/XXX
archivo_para_borrar = directorio_actual.parent.parent / "back" / "querys" / f"{nombre_clase}.py"
borrarArchivo(archivo_para_borrar)

# Ruta back/routers/XXX
archivo_para_borrar = directorio_actual.parent.parent / "back" / "routers" / f"{nombre_clase}.py"
borrarArchivo(archivo_para_borrar)

