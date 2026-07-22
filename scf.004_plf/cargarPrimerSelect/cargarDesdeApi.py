
import json
from pathlib import Path

# Configuración (en producción usar sys.argv)

# Pedir datos al usuario
modelDestino = input("Ingrese el nombre del modelo de destino (ej. rubricas): ").strip()
ModeloOrigen = input("Ingrese el nombre del modelo de origen (ej. tomos): ").strip().capitalize()
campoDestino = input("Ingrese el nombre del campo de destino (ej. tomo): ").strip()
campoOrigenListar = input("Ingrese el nombre del campo del modelo de origen que será opción (ej. nombre): ").strip()

# Capitalizar el nombre del modelo de destino
ModeloDestino = modelDestino.capitalize()

# modelDestino = "rubricas"
# ModeloOrigen = "tomos".capitalize()
# campoDestino = "tomo"
# ModeloDestino = modelDestino.capitalize()
# campoOrigenListar = "nombre"

# Rutas
directorio_actual = Path(__file__).resolve().parent
diccModeloDestino = directorio_actual.parent / "agregarModeloFuentes" / "diccModelo" / f"{modelDestino}.json"
# Rutas de archivos
src_file = (
    directorio_actual.parent.parent / "front" / "src" / "components" / 
    ModeloDestino / f"Editar{ModeloDestino}.jsx"
)

dest_file = src_file.parent / "e.jsx"  # ¿Por qué guardas en e.jsx?


def cargar_desde_api():
    
    # Obtener nombre del arreglo desde JSON
    with diccModeloDestino.open("r", encoding="utf-8") as archivo:
        arreglo_campos = json.load(archivo)
        
    nombreArreglo = next(
        (campo["optionsKey"] for campo in arreglo_campos 
        if campo["type"] == "select" and campo["name"] == campoDestino),
        None
    )

    if not nombreArreglo:
        print(f"No se encontró campo select con nombre '{campoDestino}'")
        return []
    else:


        # Procesar archivo JSX
        with src_file.open("r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        # Buscar y reemplazar
        for i, linea in enumerate(lineas):
            if f'"{nombreArreglo}": []' in linea:
                lineas[i] = f'\t"{nombreArreglo}": {nombreArreglo.capitalize()},\n'
                break
        else:
            print(f"No se encontró el arreglo '{nombreArreglo}' en {src_file}")
            return []   

        return lineas, nombreArreglo.capitalize()

def insertar_codigo(contenido, patron, codigo, insertar_antes=False):
    p = next((i for i, linea in enumerate(contenido) if patron in linea), None)
    if p is not None:
        if insertar_antes:
            contenido = contenido[:p] + [codigo] + contenido[p:]
        else:
            contenido = contenido[:p+1] + [codigo] + contenido[p+1:]
    return contenido

contenido, NombreArreglo = cargar_desde_api()

# if contenido:
#     print("Contenido cargado correctamente.")
    
# else:
#     print("No se pudo cargar el contenido.")
#
# Guardar cambios



#   patron = 'const user = useSelector((state) => state.acceso.user);'
codigo_nuevo = "\tconst { data: !NombreArreglo! = [] } = useGetDistinct!ModeloOrigen!Query('!campoOrigenListar!');\n"
codigo_nuevo = codigo_nuevo.replace("!NombreArreglo!", NombreArreglo).replace("!ModeloOrigen!", ModeloOrigen).replace("!campoOrigenListar!", campoOrigenListar)
contenido = insertar_codigo(contenido, 'const user = useSelector((state) => state.acceso.user);', codigo_nuevo, insertar_antes=True)       
# print("Código a insertar:", codigo_nuevo)
codigo_nuevo = "import { useGetDistinct!ModeloOrigen!Query } from '../../store/apiSlice';\n"
codigo_nuevo = codigo_nuevo.replace("!ModeloOrigen!", ModeloOrigen)
contenido = insertar_codigo(contenido, 'import { useSelector, useDispatch } from "react-redux";', codigo_nuevo, insertar_antes=True)    

# Guardar el archivo modificado    
with src_file.open("w", encoding="utf-8") as archivo:
    archivo.writelines(contenido)