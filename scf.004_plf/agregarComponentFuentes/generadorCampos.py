import json
from pathlib import Path

def definir_campos(nombre_clase):
    # Ruta actual
    directorio_actual = Path(__file__).resolve().parent

    # Ruta del archivo JSON
    ruta_archivo_json = directorio_actual.parent / "agregarModeloFuentes" / "diccModelo" / f"{nombre_clase}.json"
 
    # Mapeo de tipos
    tipo_mapeo = {
        "int": "number",
        "str": "text",
        "bool": "checkbox",
        "date": "date",
        "datetime": "date",
        "file": "file",
        "select": "select",
    }

    # Leer y cargar el contenido del archivo JSON
    with ruta_archivo_json.open("r", encoding="utf-8") as archivo:
        arreglo_campos = json.load(archivo)

    # Generar el formato deseado
    arreglo = []
    for campo in arreglo_campos:
        name = campo["name"]
        label = campo["label"]
        tipo = campo["type"]
        placeholder = campo.get("placeholder", f"Ingrese {label}")
        tipo_mapeado = tipo_mapeo.get(tipo, tipo)
        
        # Construir la parte base del objeto
        objeto_parts = [
            f'name: "{name}"',
            f'label: "{label}"',
            f'placeholder: "{placeholder}"',
            f'type: "{tipo_mapeado}"'
        ]
        
        # Agregar optionsKey si es un campo select
        if tipo == "select" and "optionsKey" in campo:
            objeto_parts.append(f'optionsKey: "{campo["optionsKey"]}"')
        
        # Unir todas las partes
        objeto = f'\t{{{", ".join(objeto_parts)}}},\n'
        arreglo.append(objeto)
    
    return arreglo

