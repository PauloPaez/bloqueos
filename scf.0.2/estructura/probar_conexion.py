import sys
import re

from database import database


# ---- Modelo recibido ----
model = sys.argv[1]
model_cap = model.capitalize()

print('Modelo recibido:', model.lower())
print('-------------------------------')


# ---- Función ----
def opciones_menu(componente, path):
    result = database.Rutas.insert_one({
        'componente': componente,
        'path': path,
        'nombre': re.sub(r'(?<!^)([A-Z])', r' \1', componente),
        'activo': True,
        'app': False
    })

    print('Agregar path para el menu:', result.inserted_id)


# ---- Inserciones ----
for accion in ('Actualizar', 'Listar'):
    componente = f'{accion}{model_cap}'
    path = f'/{model_cap}/{componente}'

    opciones_menu(componente, path)

    print('-------------------------------')
