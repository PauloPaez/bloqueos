from pathlib import Path
import sys
""" Lee un template de los endpoint basicos GET, POST, POST y los agrega en apiSlice.jsx
ademas los tagType y los exporta al final """
directorio_actual = Path(__file__).resolve().parent
templateEP = directorio_actual / "templates" / "endpoint.txt"

endpoint_url = sys.argv[1].lower()
endpoint = endpoint_url.capitalize()

# Directorio destino
directorio_actual = Path(__file__).resolve().parent
directorio_contiene_a_front = ((directorio_actual.parent).parent)
apiSlice = directorio_contiene_a_front/ "front" / "src" / "store" / "apiSlice.jsx"

# Leer y procesar templateEndPoint
with open(templateEP, 'r', encoding='utf-8') as f:
    lineas = f.readlines()

actualizados = [linea.replace("!endpoint!", endpoint) for linea in lineas]
lineas = [linea.replace("!endpoint_url!", endpoint_url) for linea in actualizados]

with open(apiSlice, 'r', encoding='utf-8') as f:
    sliceLineas = f.readlines()

# Procesar endpoints
p = next((i for i, dato in enumerate(sliceLineas) if "endpoints: (builder) => ({" in dato.strip()), len(sliceLineas)) + 1
sliceLineas = sliceLineas[:p] + lineas + sliceLineas[p:]

cadena_a_buscar = "tagTypes: ["
p = next((i for i, dato in enumerate(sliceLineas) if cadena_a_buscar in dato.strip()), len(sliceLineas))
lineaAbierta = sliceLineas[p][:-3]
sliceLineas[p] = f'{lineaAbierta}"{endpoint}",],\n'

cadena_a_buscar = "export const {"
p = next((i for i, dato in enumerate(sliceLineas) if cadena_a_buscar in dato.strip()), len(sliceLineas)) + 1
lista = [f"\tuseGet{endpoint}Query,\n", f"\tusePost{endpoint}Mutation,\n", f"\tusePut{endpoint}Mutation,\n",
         f"\tusePatch{endpoint}Mutation,\n",f"\tusePost{endpoint}ByFieldMutation,\n",
         f"\tuseGetDistinct{endpoint}Query,\n"]
sliceLineas = sliceLineas[:p] + lista + sliceLineas[p:]

with open(apiSlice, 'w', encoding='utf-8') as f:
	f.writelines(sliceLineas)



