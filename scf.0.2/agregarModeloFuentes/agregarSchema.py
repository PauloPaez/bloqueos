from pathlib import Path
import json
import sys 

# Nombre de la función y archivo a generar
nombre_funcion = sys.argv[1].lower()

#Ruta actual
directorio_actual = Path(__file__).resolve().parent

# Ruta del archivo JSON
ruta_archivo_json = directorio_actual / "diccModelo" /f"{nombre_funcion}.json"

# Ruta back/schemas/archivo_nuevo
ruta_schema_nuevo = directorio_actual.parent.parent / "back" / "scripts" / "schemas" / f"{nombre_funcion}.py"

# Leer y cargar el contenido del archivo JSON
with ruta_archivo_json.open("r", encoding="utf-8") as archivo:
    arreglo_campos = json.load(archivo)

# Generar el contenido de la función schema
campos_funcion = ['        "id": str(item.get("_id")),']  # Agregar 'id' al inicio
for campo in arreglo_campos:
    name = campo["name"]
    campos_funcion.append(f'        "{name}": item.get("{name}"),')

# Crear el contenido final del archivo
contenido_schema = f"""def {nombre_funcion}Sh(item):
    return {{
{chr(10).join(campos_funcion)}
    }}
"""

# Escribir el contenido a un archivo

ruta_schema_nuevo.write_text(contenido_schema, encoding="utf-8")

print(f"Archivo de schema generado en: {ruta_schema_nuevo.resolve()}")


