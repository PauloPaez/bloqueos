import sys
from pathlib import Path
from generadorCampos import definir_campos
from generdorFromulario import generar_formulario_campos

# Recibir nombre Modelo
model_lower =  sys.argv[1].lower()
model_capitalized = model_lower.capitalize()

# Directorio y archivo destino
directorio_actual = Path(__file__).resolve().parent
directorio_componente = ((directorio_actual.parent).parent) / "front" / "src" / "components" / model_capitalized
Path(directorio_componente).mkdir(parents=True, exist_ok=True)
componente = directorio_componente / f"Listar{model_capitalized}.jsx"

# Diretorio Template
templateLt = directorio_actual / "templates" / "listar.txt"

with open(templateLt, 'r', encoding='utf-8') as f:
    mainLineas = f.readlines()

# **Eliminar líneas vacías** #
mainLineas = [linea for linea in mainLineas if linea.strip()]  # Filtrar líneas no vacías

# Poner nombre del modelo en el template
a_buscar_lower = "!model!"
a_buscar_capitalized = "!Model!"

for index, linea in enumerate(mainLineas):
    # Comprobar si la línea contiene cualquiera de las dos cadenas
    if a_buscar_lower in linea or a_buscar_capitalized in linea:
        # Reemplazar ambas versiones en la línea
        mainLineas[index] = linea.replace(a_buscar_lower, model_lower).replace(a_buscar_capitalized, model_capitalized)

# Agregar los campos al formulario 
# campos = definir_campos(model_lower)
# cadena_a_buscar = "const formFields = ["
# p = next((i for i, dato in enumerate(mainLineas) if cadena_a_buscar in dato.strip()), len(mainLineas)) + 1
# mainLineas = mainLineas[:p] + campos + mainLineas[p:]

# Imprimir el resultado final

with open(componente, 'w', encoding='utf-8') as f:
	f.writelines(mainLineas)

generar_formulario_campos(model_lower, "Listar")

