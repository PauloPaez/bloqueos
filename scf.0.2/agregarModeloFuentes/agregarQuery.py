import sys
from pathlib import Path

# Recibir nombre Modelo
model = sys.argv[1]
# print(model)
# Directorio destino
directorio_actual = Path(__file__).resolve().parent
directorio_contiene_a_back = ((directorio_actual.parent).parent)
querys_dir = directorio_contiene_a_back / "back" / "scripts" /"querys"
query_py = querys_dir / f"{model}.py"

# Diretorio Template
templateQy = directorio_actual / "templates" / "query.txt"

with open(templateQy, 'r', encoding='utf-8') as f:
    queryLineas = f.readlines()

a_buscar_lower = "!model!"
a_buscar_capitalized = "!Model!"

for index, linea in enumerate(queryLineas):
    # Comprobar si la línea contiene cualquiera de las dos cadenas
    if a_buscar_lower in linea or a_buscar_capitalized in linea:
        # Reemplazar ambas versiones en la línea
        queryLineas[index] = linea.replace(a_buscar_lower, model).replace(a_buscar_capitalized, model.capitalize())
        
# Imprimir el resultado final
with open(query_py, 'w', encoding='utf-8') as f:
	f.writelines(queryLineas)
