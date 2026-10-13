import json
from pathlib import Path

# Input de datos
# Solicitar datos por teclado
# modeloOrigen = input("Ingrese el nombre del modelo donde se buscará: ").lower()
# modeloDestino = input("Ingrese el nombre del modelo donde se inserta código: ").lower()
# campo = input("Ingrese el nombre del campo a buscar: ").lower()
# *********************************
modeloOrigen = "Tipos_de_notas"
campoPrimario = "categoria"
campoSecundario = "tipo"
modeloDestino = "Tipos_de_notas"
# *********************************

nombre_componente = modeloDestino.capitalize()  # Primera letra mayúscula
# Directorios Raiz y del modelo
directorio_actual = Path(__file__).resolve().parent
ruta_diccionario = directorio_actual.parent / "agregarModeloFuentes" / "diccModelo"
#***********************************************************************************
def leer_plantillas():
    archivos = {
        "cagarArreglos": "./templates/cargarArreglos.txt",
        # "declararSelects": "./templates/declararSelect.txt",
        # "input": "./templates/inputConEnter.txt",
        #"importar": "./templates/import_usePost_Modelo.txt",
        #"constPost": "./templates/const_postModelByField.txt",
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

    return contenidos[0], contenidos[1], #contenidos[2], contenidos[3], contenidos[4]
    
#*************************************************************************************

cargarArreglos, declararSelects = leer_plantillas()

cargarArreglos = cargarArreglos.replace("!campoPrimario!", campoPrimario)
cargarArreglos = cargarArreglos.replace("!CampoPrimario!", campoPrimario.capitalize())
cargarArreglos = cargarArreglos.replace("!campoSecundario!", campoSecundario)
cargarArreglos = cargarArreglos.replace("!CampoSecundario!", campoSecundario.capitalize())
cargarArreglos = cargarArreglos.replace("!ModelOrigen!", modeloDestino.capitalize())

#declararSelects = declararSelects.replace("!campoPrimario!", campoPrimario)
#declararSelects = declararSelects.replace("!CampoPrimario!", campoPrimario.capitalize())
#declararSelects = declararSelects.replace("!campoSecundario!", campoSecundario)
#declararSelects = declararSelects.replace("!CampoSecundario!", campoSecundario.capitalize())

print(declararSelects)
