import re
import sys
from pathlib import Path

def eliminar_lineas_archivo(archivo, texto_a_eliminar):
	#Lineas a eliminar
	texto_a_eliminar_cap = texto_a_eliminar.capitalize()
	lineas_a_eliminar = []
	lineas_a_eliminar.append(f'from routers.ordenestrabajos import {texto_a_eliminar}') 
	lineas_a_eliminar.append(f'app.include_router(ordenestrabajos, tags=["{texto_a_eliminar_cap}"])' )
	# Expresión regular para buscar la lista en la línea "if entity not in [...]"
	patron_lista = re.compile(r'if entity not in \[(.*?)\]:')
	# Leer el contenido del archivo línea por línea
	with open(archivo, 'r') as file:
		lineas = file.readlines()
  
	lineas_modificadas = []
	for linea in lineas:
		match = patron_lista.search(linea)
		if match:
			# Extraer los elementos de la lista y eliminarlos si coinciden con el elemento a eliminar
			lista_elementos = match.group(1).split(',')
			lista_elementos = [e.strip().strip('"') for e in lista_elementos if e.strip().strip('"') != texto_a_eliminar]
			# Reconstruir la línea sin el elemento eliminado
			nueva_lista = ', '.join(f'"{e}"' for e in lista_elementos if e)
			linea = f'    if entity not in [{nueva_lista}]:\n'
		lineas_modificadas.append(linea)
	
	# Filtrar las líneas que no se quieren eliminar
	lineas_filtradas = [
		linea for linea in lineas_modificadas
		if not any(linea_a_eliminar in linea for linea_a_eliminar in lineas_a_eliminar)
		]
    
	# Escribir el contenido actualizado en el archivo
	with open(archivo, 'w') as file:
		file.writelines(lineas_filtradas)
    
	print(f'Líneas eliminadas del archivo: {lineas_a_eliminar}')

# Nombre de la clase a generar
texto_a_eliminar = sys.argv[1].lower()

# Directorio destino main.py
directorio_actual = Path(__file__).resolve().parent
directorio_contiene_a_back = ((directorio_actual.parent).parent)
main = directorio_contiene_a_back / "back" / "main.py"
eliminar_lineas_archivo(main, texto_a_eliminar)

