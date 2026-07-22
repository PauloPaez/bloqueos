import sys
import json
from pathlib import Path
from typing import Optional, Any, List  # Importar List para el tipo list[str]

# Mapeo de tipos de campo a tipos de Python
tipo_mapeo = {
    "int": "Optional[int]",
    "str": "Optional[str]",
    "bool": "Optional[bool]",
    "datetime": "Optional[datetime]",
    "file": "Optional[str]",
    "list": "Optional[List[str]]"
}

# Nombre de la clase a generar
nombre_clase = sys.argv[1].lower()

# Ruta actual
directorio_actual = Path(__file__).resolve().parent

# Ruta del archivo JSON
ruta_archivo_json = directorio_actual / "diccModelo" / f"{nombre_clase}.json"

# Ruta back/scripts/models/XXX
ruta_modelo_nuevo = (
    directorio_actual.parent.parent
    / "back"
    / "scripts"
    / "models"
    / f"{nombre_clase}.py"
)

# Leer JSON
with ruta_archivo_json.open("r", encoding="utf-8") as archivo:
    arreglo_campos = json.load(archivo)

# Generar campos
campos_modelo = [
    "    id: Optional[str] = Field(default=None)  # ID del documento"
]

for campo in arreglo_campos:
    name = campo["name"]
    tipo = campo["type"]
    tipo_mapeado = tipo_mapeo.get(tipo, "Optional[str]")

    if tipo == "list":
        default_value = "default=[]"
    elif tipo == "bool":
        default_value = "default=False"
    else:
        default_value = "default=None"

    campos_modelo.append(
        f"    {name}: {tipo_mapeado} = Field({default_value})"
    )

# Contenido final del modelo
contenido_modelo = f"""from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class {nombre_clase.capitalize()}(BaseModel):
{chr(10).join(campos_modelo)}

    @field_validator('*', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v
"""

# Escribir archivo
with ruta_modelo_nuevo.open("w", encoding="utf-8") as archivo:
    archivo.write(contenido_modelo)

print(f"Modelo {nombre_clase.capitalize()} generado en {ruta_modelo_nuevo}")
