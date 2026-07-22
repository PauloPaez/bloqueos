import sys

DB = sys.argv[1].upper()

actualizarRuta = f"""from pathlib import Path
import sys
from pymongo import MongoClient

ruta_conf_motor = Path(__file__).resolve().parent.parent / 'back' / 'conf'
sys.path.append(str(ruta_conf_motor))

client = MongoClient('mongodb+srv://paulo:Paulo2023@cluster0.prraayx.mongodb.net/{DB}?retryWrites=true&w=majority') 
database = client['{DB}'] 

def opciones_menu(modelo, path):
    coleccion = database.Rutas
    result = coleccion.insert_one({{'componente': modelo, 'path': path, 'activo': True}})
    print('Agregar path para el menu: ', result.inserted_id)
"""

print(actualizarRuta)
