import sys
from pathlib import Path
# from generadorCampos import definir_campos

# Recibir nombre Modelo
model_lower =  sys.argv[1].lower()
model_capitalized = model_lower.capitalize()

# Directorio y archivo destino
directorio_actual = Path(__file__).resolve().parent
directorio_componente = ((directorio_actual.parent).parent) / "front" / "src" / "components" / model_capitalized
Path(directorio_componente).mkdir(parents=True, exist_ok=True)
componente = directorio_componente / f"Select{model_capitalized}.jsx"

# Diretorio Template
templateEr = directorio_actual / "templates" / "select.txt"

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
