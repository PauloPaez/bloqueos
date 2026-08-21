import sys
from pathlib import Path
import json
from pprint import pformat

# Recibir nombre Modelo
model_lower = sys.argv[1].lower()
model_capitalized = model_lower.capitalize()

# Directorios Raiz y del modelo
directorio_actual = Path(__file__).resolve().parent
ruta_archivo_json = directorio_actual.parent / "agregarModeloFuentes" / "diccModelo" / f"{model_lower}.json"

# Leer y cargar el contenido del archivo JSON
with ruta_archivo_json.open("r", encoding="utf-8") as archivo:
    arreglo_campos = json.load(archivo)

# Mapeo de tipos
type_map = {
    "text": "str",
    "number": "number",
    "date": "date",
    "bool": "checkbox"
}

filtros = []
for field in arreglo_campos:
    if field.get("placeholder") == "no_visible":
      continue
    # Set default value for checkbox to true
    valor_inicial = True if field["type"] == "checkbox" else ""
    
    filtros.append({
        "etiqueta": field["label"],
        "clave": field["name"],
        "valor": valor_inicial,
        "tipo": type_map.get(field["type"], field["type"]),
        "placeholder": field["placeholder"]
    })

# Generate component content
component_content = f"""import React from 'react';
import GenericFilter from '../../common/GenericFilter';

const Filtro{model_capitalized} = ({{ filtroInicial, postFijo }}) => {{
  const configuracionFiltro = [
"""

# Add each filter item
for item in filtros:
    item_str = pformat(item, indent=4, width=80)
    component_content += f"    {item_str},\n"

# Add the rest of the component
component_content += f"""];
  
  return (
    <GenericFilter
      configuracion={{configuracionFiltro}}
      filtroInicial={{filtroInicial}}
      postFijo={{postFijo}}
      claveFiltro="{model_lower}"
    />
  );
}};

export default Filtro{model_capitalized};
"""

# Create the component directory if it doesn't exist
directorio_componente = ((directorio_actual.parent).parent) / "front" / "src" / "components" / model_capitalized
Path(directorio_componente).mkdir(parents=True, exist_ok=True)
componente = directorio_componente / f"Filtro{model_capitalized}.jsx"

# Save the component file
with componente.open("w", encoding="utf-8") as archivo:
    archivo.write(component_content)

print(f"Componente Filtro{model_capitalized} generado exitosamente en:")
print(componente)
