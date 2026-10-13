import sys
import json
from pathlib import Path

# modelDestino = sys.argv[1].lower()
# campoDestino = sys.argv[2].lower()
modelDestino = "rubricas"
campoDestino = "libro"
ModeloDestino = modelDestino.capitalize()
# Ruta actual
directorio_actual = Path(__file__).resolve().parent
diccModeloDestino = directorio_actual.parent / "agregarModeloFuentes"  / "diccModelo" / f"{modelDestino}.json"

# Leer y cargar el contenido del archivo JSON
with diccModeloDestino.open("r", encoding="utf-8") as archivo:
    arreglo_campos = json.load(archivo)
    
for campo in arreglo_campos:
    name = campo["name"]
    tipo = campo["type"]
    if tipo == "select" and name == campoDestino:
        nombreArreglo = campo["optionsKey"]
        

Modelodd = directorio_actual.parent.parent / "front" / "src" / "components" / ModeloDestino  / f"Editar{ModeloDestino }.jsx"    
ModeloDestino = directorio_actual.parent.parent / "front" / "src" / "components" / ModeloDestino  / "e.jsx"

# Leer y cargar el contenido del componente JSX

with open(Modelodd, "r", encoding="utf-8") as archivo:
    contenido = archivo.readlines()
    

for i, linea in enumerate(contenido):
    if f'"{nombreArreglo}": []' in linea:
      #print(f"Encontrado en la línea {i}: {linea.strip()}")
      break
if i < len(contenido):
    # Reemplazar la línea encontrada con un comentario
    contenido[i] = f'\t"{nombreArreglo}": {nombreArreglo.capitalize()},\n'

print(ModeloDestino)

with open(ModeloDestino, "w", encoding="utf-8") as archivo:
  archivo.writelines(contenido) 




