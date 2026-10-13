import json
from pathlib import Path

# Rutas
directorio_actual = Path(__file__).resolve().parent

"""Script para agregar select con filtro en componente Editar<ModuloDestino>.jsx
   basado en un archivo JSON con criterios y código a insertar.
   El archivo JSON debe tener la estructura:
   [
     {
       "criterio": "línea de búsqueda",         
       "axn": "antes|despues|reemplazar",
        "codigoNuevo": "código a insertar"
        },
        ...
    ]
"""
# ===============================================
moduloOrigen = input("Modulo Origen de los datos: ").lower()
moduloDestino =  input("Modulo donde es el formulario con el select: ").lower()
ModuloDestino = moduloDestino.capitalize()
# ----------------------------------------------
campoMostrar = input("nombre de campo que aparecerá en select: ").lower()
campoDestino = input("nombre de campo done se gruardará el valor seleccionado: ").lower()
# ----------------------------------------------
filtro = input("Filtro en formato JSON usa comillas DOBLES:")
# ================================================

replacements = {
    "!ModuloOrigen!": moduloOrigen.capitalize(),
    "!moduloDestino!": moduloDestino,
    "!ModuloDestino!": moduloDestino.capitalize(),
    "!campoMostrar!": campoMostrar,
    "!filtroDatosOrigen!": "{'activo': True}",
    "!campoDestino!": campoDestino,
    "!CampoDestino!": campoDestino.capitalize(),
    "!filtro!": filtro.strip()
}
# Rutas de componente Editar<ModuloDestino>.jsx
src_file = (
    directorio_actual.parent.parent / "front" / "src" / "components" / 
    ModuloDestino / f"Editar{ModuloDestino}.jsx"
)
# Leer el archivo fuente
with src_file.open("r", encoding="utf-8") as archivo:
    contenidoComponente = archivo.readlines()
    
# ----------Leer el archivo JSON------------------------
with open('templates/codigo.json', 'r', encoding='utf-8') as file:
    arregloCodigo = json.load(file)
#-----------------------------------------------------

def insertarCodigoEnComponente(contenidoComponente, criterio, axn, codigo):
    p = next((i for i, linea in enumerate(contenidoComponente) if criterio in linea), None)
    if p is not None:
        if axn == "antes":
            contenidoComponente = contenidoComponente[:p] + [codigo] + contenidoComponente[p:]
        else:
            if axn == "despues":
                contenidoComponente = contenidoComponente[:p+1] + [codigo] + contenidoComponente[p+1:]
            if axn == "reemplazar": 
                contenidoComponente[p] = codigo
    return contenidoComponente

def reemplazarPalabras(codigoNuevo):
    if isinstance(codigoNuevo, list):  
        # unir el array de líneas en un bloque
        codigoNuevo = "\n".join(codigoNuevo) + "\n"
    for marcador, valor in replacements.items():
        codigoNuevo = codigoNuevo.replace(marcador, valor)
    return codigoNuevo

# Procesar como antes
for codigo in arregloCodigo:
    # print("Procesando criterio:", codigo['criterio'])
    codigo['criterio'] = reemplazarPalabras(codigo['criterio'])
    codigo['codigoNuevo'] = reemplazarPalabras(codigo['codigoNuevo'])
    
for codigo in arregloCodigo:
    contenidoComponente = insertarCodigoEnComponente(
        contenidoComponente, 
        codigo['criterio'], 
        codigo['axn'], 
        codigo['codigoNuevo']
    )

for x in contenidoComponente:
     print(x)

seguir = input('Queres Modificar el Editar<Componente>.jsx (s/n)')
if seguir == 's': 
    # Guardar el archivo modificado    
    with src_file.open("w", encoding="utf-8") as archivo:
     archivo.writelines(contenidoComponente)
