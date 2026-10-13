from pathlib import Path
import sys
import re
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# ---- Cargar variables de entorno desde back/.env ----
ruta_env = Path(__file__).resolve().parent.parent.parent / 'back' / '.env'
print('*********************Ruta del archivo .env:', ruta_env)
load_dotenv(dotenv_path=ruta_env)

# ---- Configuración de paths ----

ruta_conf_motor = Path(__file__).resolve().parent.parent / 'back' / 'scripts' / 'conf'
print('Ruta de configuración del motor:', ruta_conf_motor)
sys.path.append(str(ruta_conf_motor))

# ---- Base de datos ----
mongo_uri = os.getenv("MONGO_URI")
nombre_base = os.getenv("MONGO_DB")

if not mongo_uri or not nombre_base:
    raise RuntimeError("Faltan MONGO_URI o MONGO_DB en el archivo .env")

print('Base de datos por defecto:', nombre_base)


client = MongoClient(mongo_uri)
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
