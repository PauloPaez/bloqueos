import json
from pathlib import Path

# Directorios Raiz y del modelo
directorio_actual = Path(__file__).resolve().parent
ruta_diccionario = directorio_actual.parent / "agregarModeloFuentes" / "diccModelo" 

# Solicitar datos por teclado
modeloOrigen = input("Ingrese el nombre del modelo donde se buscará: ").lower()
modeloDestino = input("Ingrese el nombre del modelo donde se inserta código: ").lower()
campo = input("Ingrese el nombre del campo a buscar: ")  #.lower()
# modeloOrigen = 'empleados'
# modeloDestino = 'accidentes'
# campo = 'dni'
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
    return subConjunto

#--------------------BuscarDatos_x_Campo---------------------------------  
def generar_buscar_x_campo(modeloOrigen,campo):

    # Procesar las variables según requerimientos
    Modelo = modeloOrigen.capitalize()  # Primera letra mayúscula
    Campo = campo.capitalize()
    
    # Leer el archivo plantilla
    try:
        with open('buscarPorCampo.txt', 'r', encoding='utf-8') as file:
            contenido = file.read()
    except FileNotFoundError:
        print("Error: El archivo 'plantilla.txt' no se encontró.")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    # Realizar los reemplazos
    contenido = contenido.replace('!Model!', Modelo)
    contenido = contenido.replace('!model!', modeloOrigen)
    contenido = contenido.replace('!campo!', campo)
    contenido = contenido.replace('!Campo!', Campo)
    # Generar nombre del archivo de salida
    nombre_archivo_salida = f"buscar_{campo}.js"
    
    # Escribir el archivo resultante
    try:
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as file:
            file.write(contenido)
    except Exception as e:
        print(f"Error al escribir el archivo: {e}")

    print(contenido)
#------------------ActualizarFormulario---------------------------
def generar_actualizarFromulario(camposComunes,modeloOrigen):
    # Leer el archivo plantilla
    try:
        with open('cargarFormulario.txt', 'r', encoding='utf-8') as file:
            contenido = file.read()
    except FileNotFoundError:
        print("Error: El archivo 'cargarFormulario.txt' no se encontró.")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
     
    # Convertir la lista a una cadena con formato de array JavaScript
    campos_str = "['" + "', '".join(camposComunes) + "']"
    # Realizar los reemplazos
    contenido = contenido.replace('!camposInterseccion!', campos_str)
    contenido = contenido.replace('!model!', modeloOrigen)
    print( contenido)

#-------INPUT + ENTER---- Para insertar en EditarModelo---------------------
def generarInputConEnter():
    # Leer el archivo plantilla
    try:
        with open('inputConEnter.txt', 'r', encoding='utf-8') as file:
            contenido = file.read()
    except FileNotFoundError:
        print("Error: El archivo 'inputConEnter.txt' no se encontró.")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
     
    # Realizar los reemplazos
    contenido = contenido.replace('!campo!', campo)
    contenido = contenido.replace('!Campo!', campo.capitalize())
    
    # en la variable contenido está la porción de codigo para insertar despues de:
    #'            className={`form-input ${formField.type === "checkbox" ? "form-check-input" : "form-control"}`}'
    # en el archivo de componente *modeloDestino*
    
    print( contenido)
   
    # debajo de import { resetFila } from "../../store/appSlice";
    post = "import { post!Model!ByField } from usePost!Model!ByFieldMutation();" 
    post = post.replace('!Model',modeloOrigen.capitalize())
    
    # debajo de const [patchReportes] = usePatchReportesMutation(); // Importar la mutación PATCH
    const = "const [post!Model!ByField] = usePost!Model!ByFieldMutation();"
    const = const.replace('!Model!',modeloOrigen.capitalize())

#-----------------------------------------------------------------
#                       Principal
#-----------------------------------------------------------------
diccionario_origen =  ruta_diccionario / f"{modeloOrigen}.json" 
diccionario_destino =  ruta_diccionario / f"{modeloDestino}.json" 
# verificar que exiten los archivos de diccionarios
if not diccionario_origen.exists():
    print(f"Error: No se encontró el diccionario de origen: {diccionario_origen}")
    exit(1)
if not diccionario_destino.exists():
    print(f"Error: No se encontró el diccionario de destino: {diccionario_destino}")
    exit(1)
camposComunes = interseccion(diccionario_origen, diccionario_destino)   
generar_actualizarFromulario(camposComunes,modeloDestino) 
generar_buscar_x_campo(modeloOrigen,campo)
generarInputConEnter()
#generadorActualizarFormulario(modelo_origen, camposComunes) # ---->> Bloque Buscar Datos


#buscarReportes---
