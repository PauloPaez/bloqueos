import json
from pathlib import Path

# Input de datos
# Solicitar datos por teclado
modeloOrigen = input("Ingrese el nombre del modelo donde se buscará: ").lower()
modeloDestino = input("Ingrese el nombre del modelo donde se inserta código: ").lower()
campo = input("Ingrese el nombre del campo a buscar: ").lower()
# *********************************
# modeloOrigen = "cooperativas"
# campo = "cuit"
# modeloDestino = "rubricas"
# *********************************

nombre_componente = modeloDestino.capitalize()  # Primera letra mayúscula
# Directorios Raiz y del modelo
directorio_actual = Path(__file__).resolve().parent
ruta_diccionario = directorio_actual.parent / "agregarModeloFuentes" / "diccModelo"
ruta_componente = (
    directorio_actual.parent.parent
    / "front"
    / "src"
    / "components"
    / nombre_componente
    / f"Editar{nombre_componente}.jsx"
)
# Fin Directorios


# ------------------------Intersección----------------------------


def arregloCampos(modelo):
    with modelo.open("r", encoding="utf-8") as archivo:
        arreglo_campos = json.load(archivo)
    filtro = []
    for field in arreglo_campos:
        filtro.append(field["name"])
    return filtro

def interseccion(modeloOrigen, modeloDestino):
    arregloOrigen = arregloCampos(modeloOrigen)
    arregloDestino = arregloCampos(modeloDestino)
    subConjunto = list(set(arregloOrigen) & set(arregloDestino))
    return str(subConjunto)


# ------------------------Insertar Codigo---------------------------

def insertar_codigo(contenido, patron, codigo, insertar_antes=True):
    p = next((i for i, linea in enumerate(contenido) if patron in linea), None)
    if p is not None:
        if insertar_antes:
            contenido = contenido[:p] + [codigo] + contenido[p:]
        else:
            contenido = contenido[:p+1] + [codigo] + contenido[p+1:]
    return contenido

#***********************************************************************************
def leer_plantillas():
    archivos = {
        "buscar": "./templates/buscarPorCampo.txt",
        "formulario": "./templates/cargarFormulario.txt",
        "input": "./templates/inputConEnter.txt",
        "importar": "./templates/import_usePost_Modelo.txt",
        "constPost": "./templates/const_postModelByField.txt",
    }

    contenidos = []    

    for clave, ruta in archivos.items():
        try:
            with open(ruta, "r", encoding="utf-8") as file:
                contenido = file.read()
            contenidos.append(contenido)
        except FileNotFoundError:
            print(f"Error: El archivo '{ruta}' no se encontró.")
            return
        except Exception as e:
            print(f"Error al leer el archivo '{ruta}': {e}")
            return

    return contenidos[0], contenidos[1], contenidos[2], contenidos[3], contenidos[4]
    

def rutas_diccionarios():
    diccionario_origen = ruta_diccionario / f"{modeloOrigen}.json"
    diccionario_destino = ruta_diccionario / f"{modeloDestino}.json"
    # verificar que exiten los archivos de diccionarios
    if not diccionario_origen.exists():
        print(f"Error: No se encontró el diccionario de origen: {diccionario_origen}")
        exit(1)
    if not diccionario_destino.exists():
        print(f"Error: No se encontró el diccionario de destino: {diccionario_destino}")
        exit(1)
    return (diccionario_origen, diccionario_destino,)

def leer__EditarComponente(ruta_componente):
    try:
        with open(ruta_componente, "r", encoding="utf-8") as file:
            contenido = file.readlines()
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_componente}' no se encontró.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []
    return contenido


# -----------------------------------------------------------------
#                       Principal
# -----------------------------------------------------------------
contenido = leer__EditarComponente(ruta_componente)
diccionario_origen, diccionario_destino = rutas_diccionarios()
camposComunes = interseccion(diccionario_origen, diccionario_destino)
buscarPorCampo, cargarFormulario,inputConEnter, importar, constPost = leer_plantillas()

cargarFormulario = cargarFormulario.replace("!camposInterseccion!", camposComunes)
cargarFormulario = cargarFormulario.replace("!model!", modeloDestino)

buscarPorCampo = buscarPorCampo.replace("!campo!", campo)
buscarPorCampo = buscarPorCampo.replace("!Campo!", campo.capitalize())
buscarPorCampo = buscarPorCampo.replace("!model!", modeloOrigen)
buscarPorCampo = buscarPorCampo.replace("!Model!", modeloOrigen.capitalize())

inputConEnter = inputConEnter.replace("!campo!", campo)
inputConEnter = inputConEnter.replace("!Campo!", campo.capitalize())
inputConEnter = inputConEnter.replace("!model!", modeloDestino)    

importar = importar.replace("!Model!", modeloOrigen.capitalize())
constPost = constPost.replace("!Model!", modeloOrigen.capitalize())

#------------INSERTAR CODIGO EN EL COMPONENTE-------------------
patron = 'disabled: field.disabled,'
contenido = insertar_codigo(contenido, patron, inputConEnter, insertar_antes=False)
patron = 'const onSubmit = async (data) => {'
contenido = insertar_codigo(contenido, patron, buscarPorCampo)
patron = 'const buscar'
contenido = insertar_codigo(contenido, patron, cargarFormulario)
patron = 'import { useSelector, useDispatch } from "react-redux";'
contenido = insertar_codigo(contenido, patron, importar)
patron = 'const dispatch = useDispatch();'
contenido = insertar_codigo(contenido, patron, constPost)

for i, linea in enumerate(contenido):
    print(linea, end='')
    
# Imprimir el resultado final
with open(ruta_componente, 'w', encoding='utf-8') as f:
    f.writelines(contenido)


