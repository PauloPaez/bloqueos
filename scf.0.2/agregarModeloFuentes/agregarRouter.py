from pathlib import Path
import sys

# Recibir nombre Modelo
model =  sys.argv[1].lower()

# Directorio destino
directorio_actual = Path(__file__).resolve().parent
directorio_contiene_a_back = ((directorio_actual.parent).parent)
router = directorio_contiene_a_back / "back" / "scripts" / "routers"  / f"{model}.py"

# Diretorio Template
templateRt = directorio_actual / "templates" / "router.txt"

with open(templateRt, 'r', encoding='utf-8') as f:
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
        mainLineas[index] = linea.replace(a_buscar_lower, model).replace(a_buscar_capitalized, model.capitalize())

# Imprimir el resultado final

with open(router, 'w', encoding='utf-8') as f:
	f.writelines(mainLineas)





