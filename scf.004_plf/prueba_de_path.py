from pathlib import Path

# Construir la ruta al directorio que contiene conf.motor usando pathlib
ruta_actual = Path(__file__).resolve().parent
print(ruta_actual)

DB = 'COOP3'

# Cadena de conexión a MongoDB usando el valor de DB
conexion = f"""
from motor.motor_asyncio import AsyncIOMotorClient

cliente = AsyncIOMotorClient('mongodb+srv://paulo:Paulo2023@cluster0.prraayx.mongodb.net/{DB}?retryWrites=true&w=majority')
database = cliente.{DB}
"""

print(conexion)


# Actualizar ruta y conexión a MongoDB
actualizarRuta = f"""
from pathlib import Path
import sys
from pymongo import MongoClient

ruta_conf_motor = Path(__file__).resolve().parent.parent / 'back' / 'conf'
sys.path.append(str(ruta_conf_motor))

client = MongoClient('mongodb+srv://paulo:Paulo2023@cluster0.prraayx.mongodb.net/{DB}?retryWrites=true&w=majority') 
database = client['{DB}'] 

def opciones_menu(modelo, path):
    coleccion = database.Opciones_menu
    result = coleccion.insert_one({{'modelo': modelo, 'path': path, 'activo': True}})
    print('Agregar path para el menu: ', result.inserted_id)
"""

print(actualizarRuta)


