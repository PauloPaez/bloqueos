import sys
from pathlib import Path
directorio_actual = Path(__file__).resolve().parent
directorio_agregar_opcion = directorio_actual.parent

# Recibir nombre Modelo
model_lower =  sys.argv[1].lower()
model_capitalized = model_lower.capitalize()

# Directorio destino
directorio_a_front = ((directorio_actual.parent).parent)
appSlice = directorio_a_front/ "front" / "src" / "store" / "appSlice.jsx"

# Leer Navbar desde el Front
with open(appSlice, 'r', encoding='utf-8') as f:
    sliceLineas = f.readlines()

# **Eliminar líneas vacías** #
sliceLineas = [linea for linea in sliceLineas if linea.strip()]

# Buscar el índice de la línea que contiene el texto
texto_buscado = '// Estructura de datos para cada módulo'
p = next((i for i, linea in enumerate(sliceLineas) if texto_buscado in linea), None) + 1
print(f"Índice de la línea que contiene '{texto_buscado}': {p}")

#Leer Template appSlice
stateModulo = directorio_actual / "templates" / "stateModulo.txt"

with open(stateModulo, 'r', encoding='utf-8') as f:
    stateModuloLineas = f.readlines()
 
stateModuloLineas = [line.replace("!model!", model_lower) for line in stateModuloLineas] 

sliceLineas = sliceLineas[:p] + stateModuloLineas + sliceLineas[p:]
# Imprimir el resultado final
with open(appSlice, 'w', encoding='utf-8') as f:
    f.writelines(sliceLineas)
    


