import sys
from pathlib import Path

# Recibir nombre Modelo
model_lower =  sys.argv[1].lower()
model_capitalized = model_lower.capitalize()

# Directorio destino
directorio_actual = Path(__file__).resolve().parent
directorio_contiene_a_front = ((directorio_actual.parent).parent)
componente = directorio_contiene_a_front/ "front" / "src" / "components" / model_capitalized / f"Actualizar{model_capitalized}.jsx"

# Diretorio Template
templateEr = directorio_actual / "templates" / "editarListar.txt"

with open(templateEr, 'r', encoding='utf-8') as f:
    mainLineas = f.readlines()

# Poner nombre del modelo en el template
a_buscar_lower = "!model!"
a_buscar_capitalized = "!Model!"

for ix, linea in enumerate(mainLineas):
    linea = linea.replace(a_buscar_lower, model_lower).replace(a_buscar_capitalized, model_capitalized)
    mainLineas[ix] = linea

# Imprimir el resultado final

with open(componente, 'w', encoding='utf-8') as f:
	f.writelines(mainLineas)
