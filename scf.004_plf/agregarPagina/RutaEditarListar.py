import sys
from pathlib import Path

# Recibir nombre Modelo
model_lower =  sys.argv[1].lower()
model_capitalized = model_lower.capitalize()

# Directorio destino
directorio_actual = Path(__file__).resolve().parent
directorio_contiene_a_front = ((directorio_actual.parent).parent)
rutas = directorio_contiene_a_front/ "front" / "src" / "routers" / "Rutas.jsx"

# Diretorio Template
templateRuta = directorio_actual / "templates" / "rutaEditarListar.txt" 

with open(templateRuta, 'r', encoding='utf-8') as f:
    templateLineas = f.readlines()  

a_buscar_lower = "!model!"
a_buscar_capitalized = "!Model!"

for index, linea in enumerate(templateLineas):
    if  a_buscar_capitalized in linea:
        templateLineas[index] = linea.replace(a_buscar_capitalized, model_capitalized)

# Leer Rutas.jsx desde el Front
with open(rutas, 'r', encoding='utf-8') as f:
    rutasLineas = f.readlines()  

# Buscar el índice de la línea que contiene el texto y AGREGAR el código
texto_buscado = "{/* Comimenza Codigo agregado por script */}"
p = next((i for i, linea in enumerate(rutasLineas) if texto_buscado in linea), None) + 1
rutasLineas = rutasLineas[:p] + templateLineas + rutasLineas[p:]



# Agregar importacion de componente LISTAR
code_import = []
code_import.append(f"import EditarListar{model_capitalized} from '../pages/EditarListar{model_capitalized}';\n")
texto_buscado = 'import Bienvenida from "../components/Bienvenida";'
p = next((i for i, linea in enumerate(rutasLineas) if texto_buscado in linea), None) + 1
rutasLineas = rutasLineas[:p] + code_import + rutasLineas[p:]

# Imprimir el resultado final
with open(rutas, 'w', encoding='utf-8') as f:
	f.writelines(rutasLineas)


















