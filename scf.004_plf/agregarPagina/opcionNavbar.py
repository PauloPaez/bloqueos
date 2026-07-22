import sys
from pathlib import Path
directorio_actual = Path(__file__).resolve().parent
directorio_agregar_opcion = directorio_actual.parent
# print("Hola desde opcionNavbar.py:", directorio_agregar_opcion)
sys.path.append(str(directorio_agregar_opcion))
import agregarRuta
# Recibir nombre Modelo
model_lower =  sys.argv[1].lower()
model_capitalized = model_lower.capitalize()

# Directorio destino

directorio_contiene_a_front = ((directorio_actual.parent).parent)
navbar = directorio_contiene_a_front/ "front" / "src" / "components" / "Navbar.jsx"

# Leer Navbar desde el Front
with open(navbar, 'r', encoding='utf-8') as f:
    navbarLineas = f.readlines()

# **Eliminar líneas vacías** #
navbarLineas = [linea for linea in navbarLineas if linea.strip()]

# Buscar el índice de la línea que contiene el texto
texto_buscado = 'title="Edición"'
p = next((i for i, linea in enumerate(navbarLineas) if texto_buscado in linea), None) + 2
codigo_agregar = []
path = f"/EditarListar/{model_lower}"
codigo_agregar.append('\t' * 3 + f'{{label: "{model_capitalized}", to: "{path}"}},\n')
agregarRuta.opciones_menu(model_lower, path)


navbarLineas = navbarLineas[:p] + codigo_agregar + navbarLineas[p:]

# Imprimir el resultado final
with open(navbar, 'w', encoding='utf-8') as f:
	f.writelines(navbarLineas)


