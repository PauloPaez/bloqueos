import re
import sys
from pathlib import Path

def eliminar_texto_archivo(archivo, texto_a_eliminar):
    # Leer el contenido del archivo
    with open(archivo, 'r') as file:
        contenido = file.read()
    
    # Eliminar el texto específico (incluye el manejo de espacios y saltos de línea)
    nuevo_contenido = re.sub(rf'"{texto_a_eliminar}": \[\],?\s*', '', contenido)
    
    # Escribir el contenido actualizado en el archivo
    with open(archivo, 'w') as file:
        file.write(nuevo_contenido)
    
    print(f'Texto "{texto_a_eliminar}" eliminado del archivo.')

# Nombre de la clase a generar
texto_a_eliminar = sys.argv[1].lower()

# Directorio destino main.py
directorio_actual = Path(__file__).resolve().parent
directorio_contiene_a_back = ((directorio_actual.parent).parent)
websocket = directorio_contiene_a_back / "back" / "utils" / "websockets_manager.py"

eliminar_texto_archivo(websocket, texto_a_eliminar)


