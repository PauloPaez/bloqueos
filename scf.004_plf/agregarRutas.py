from pathlib import Path
import sys
import re
from pymongo import MongoClient

# ---- Configuración de paths ----
ruta_conf_motor = Path(__file__).resolve().parent.parent / 'back' / 'scripts' / 'conf'
sys.path.append(str(ruta_conf_motor))

import engine  # importa engine.py directamente

# ---- Base de datos ----
nombre_base = engine.database.name
print('Base de datos por defecto:', nombre_base)

client = MongoClient(
    'mongodb+srv://paulo:Paulo2023@cluster0.prraayx.mongodb.net/ACCESOS?retryWrites=true&w=majority'
)
database = client[nombre_base]

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


