from pathlib import Path
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# ---- Cargar variables de entorno desde back/.env ----
ruta_env = Path(__file__).resolve().parent.parent.parent / 'back' / '.env'

print('Ruta del archivo .env:', ruta_env)

load_dotenv(dotenv_path=ruta_env)

# ---- Configuración de MongoDB ----
mongo_uri = os.getenv("MONGO_URI")
nombre_base = os.getenv("MONGO_DB")

print('**mongo_uri: ', mongo_uri)
print('**nombre_base', nombre_base)

if not mongo_uri or not nombre_base:
    raise RuntimeError(
        "Faltan MONGO_URI o MONGO_DB en el archivo .env"
    )

else:
    print('Base de datos por defecto:', nombre_base)

# ---- Conexión ----
client = MongoClient(mongo_uri)
database = client[nombre_base]
