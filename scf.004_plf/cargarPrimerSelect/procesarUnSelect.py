import json
from pathlib import Path

# Pedir datos al usuario
ModuloDestino = input("Modulo donde está el Select:").strip().capitalize()
ModuloOrigen = input("MODELO origen datos (ej. provincias): ").strip().capitalize()
campoOrigen = input("Campo desde donde se obtiene las opciones: ").strip().lower()
campoOpciones = input("CAMPO del select: ").strip().lower()

# Rutas
directorio_actual = Path(__file__).resolve().parent

# Rutas de archivos
src_file = (
    directorio_actual.parent.parent / "front" / "src" / "components" / 
    ModuloDestino / f"Editar{ModuloDestino}.jsx"
)

# dest_file = src_file.parent / "e.jsx"
#src_file = directorio_actual / f"Editar{ModuloDestino}.jsx"


def pluralizar(palabra):
    """Función para pluralizar palabras en español según reglas gramaticales."""
    vocales = {'a', 'e', 'i', 'o', 'u'}
    
    if not palabra:
        return palabra
    
    # Casos especiales
    if palabra.lower().endswith('z'):
        return palabra[:-1] + "ces"
    elif palabra.lower().endswith(('s', 'x')):
        return palabra + "es"
    elif palabra.lower().endswith('y') and len(palabra) > 1 and palabra[-2].lower() not in vocales:
        return palabra[:-1] + "ies"
    elif palabra.lower().endswith(('á', 'é', 'í', 'ó', 'ú')):
        return palabra + "s"
    elif palabra.lower().endswith('n') or palabra.lower().endswith('r'):
        return palabra + "es"
    else:
        return palabra + "s"
    
def valorizarPatron(arregloCodigo):
    reemplazos = {
    "!ModuloOrigen!": ModuloOrigen,
    "!campoOrigen!": campoOrigen,
    "!campoOpciones!": campoOpciones,
    "!ModuloDestino!": ModuloDestino,
    "!CampoOpcionesPl!": pluralizar(campoOpciones).capitalize(),
    "!campoOpcionesPl!": pluralizar(campoOpciones)
    }   
    
    for marcador, valor in reemplazos.items():
         arregloCodigo = arregloCodigo.replace(marcador, valor)
 
    return arregloCodigo

def insertarCodigoEnComponente(contenidoComponente, criterio, axn, codigo):
    p = next((i for i, linea in enumerate(contenidoComponente) if criterio in linea), None)
    if p is not None:
        if axn == "antes":
            contenidoComponente = contenidoComponente[:p] + [codigo] + contenidoComponente[p:]
        else:
            if axn == "despues":
                contenidoComponente = contenidoComponente[:p+1] + [codigo] + contenidoComponente[p+1:]
            else: 
                contenidoComponente[p] = codigo
            
    return contenidoComponente

# Leer el archivo JSON
with open('templates/codigos.json', 'r', encoding='utf-8') as file:
    arregloCodigo = json.load(file)

# Procesar archivo JSX
with src_file.open("r", encoding="utf-8") as archivo:
    contenidoComponente = archivo.readlines()
            
# Procesar cada entrada en el JSON
for codigo in arregloCodigo:
    # Aplicar reemplazos a cada campo del diccionario
    for key in codigo:
        if isinstance(codigo[key], str):  # Solo procesar strings
            codigo[key] = valorizarPatron(codigo[key])

for codigo in arregloCodigo:
    contenidoComponente = insertarCodigoEnComponente(contenidoComponente, codigo['criterio'], codigo['axn'], codigo['codigoNuevo'])

# for x in contenidoComponente:
#     print(x)
# Guardar el archivo modificado  
  
with src_file.open("w", encoding="utf-8") as archivo:
    archivo.writelines(contenidoComponente)
    