from pathlib import Path
import sys

def eliminarTag(apiSlice_limpio, endpoint):
    p = next((i for i, dato in enumerate(apiSlice_limpio) if 'tagTypes:' in dato), len(apiSlice_limpio))
    cadena = apiSlice_limpio[p]
    cadena = cadena.replace(f'"{endpoint}",','')
    apiSlice_limpio[p] = cadena
    return apiSlice_limpio

def elimarExportacion(apiSlice_sin_EP, endpoint):
    lineas_a_eliminar = [f"\tuseGet{endpoint}Query,\n", f"\tusePost{endpoint}Mutation,\n", f"\tusePut{endpoint}Mutation,\n"]
    pf = len(lineas_a_eliminar)
    p = next((i for i, dato in enumerate(apiSlice_sin_EP) if lineas_a_eliminar[0] in dato), len(apiSlice_sin_EP))
    sliceLineas = apiSlice_sin_EP[:p] + apiSlice_sin_EP[p + pf:]
    return sliceLineas

def eliminarEndPoints(apiSlice, templateEP, endpoint):
    
    # Leer y procesar templateEndPoint
    with open(templateEP, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    metodosCompletados = [linea.replace("!endpoint!", endpoint) for linea in lineas]
    with open(apiSlice, 'r', encoding='utf-8') as f:
        sliceOriginal = f.readlines()    
    p = next((i for i, dato in enumerate(sliceOriginal) if metodosCompletados[0] in dato), len(sliceOriginal))
    pf = len(metodosCompletados)
    sliceLineas = sliceOriginal[:p] + sliceOriginal[p + pf:]
    return sliceLineas


endpoint = sys.argv[1].lower()
endpoint_cap = endpoint.capitalize()

#Directorio Actual
directorio_actual = Path(__file__).resolve().parent

# Directorio destino apiSlice.jsx
apiSlice = ((directorio_actual.parent).parent) / "front" / "src" / "store" / "apiSlice.jsx"

# Directorio del templateEP
templateEP = (directorio_actual.parent) / "agregarModeloFuentes" / "templates" / "endpoint"

apiSlice_sin_EP = eliminarEndPoints(apiSlice, templateEP, endpoint_cap)
apiSlice_sin_Exportar = elimarExportacion(apiSlice_sin_EP, endpoint_cap)
apiSlice_limpio = eliminarTag(apiSlice_sin_Exportar, endpoint_cap)

# Escribir el contenido actualizado en el archivo
with open(apiSlice, 'w') as file:
	file.writelines(apiSlice_limpio)


