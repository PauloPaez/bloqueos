from pymongo import MongoClient
import json
from pathlib import Path

# 1. Conectar a MongoDB
conn = MongoClient('mongodb+srv://paulo:Paulo2023@cluster0.prraayx.mongodb.net/BLOQUEOS_DPI?retryWrites=true&w=majority')
db = conn['BLOQUEOS_DPI']
coleccion = db['escuelas']

# 2. Cargar el archivo padrones.json
archivo = Path('padrones.json')
if not archivo.exists():
    print(f"El archivo {archivo} no existe.")
    exit(1)

with open(archivo, 'r', encoding='utf-8') as f:
    datos = json.load(f)

# 3. Verificar que sea una lista de documentos
if not isinstance(datos, list):
    print("El archivo JSON no contiene una lista de documentos.")
    exit(1)

if not datos:
    print("El archivo está vacío, no hay documentos para insertar.")
    exit(0)

# 4. Insertar en MongoDB (con manejo de errores)
try:
    resultado = coleccion.insert_many(datos)
    print(f"✅ Se insertaron {len(resultado.inserted_ids)} documentos en la colección 'escuelas'.")
except Exception as e:
    print(f"❌ Error al insertar: {e}")