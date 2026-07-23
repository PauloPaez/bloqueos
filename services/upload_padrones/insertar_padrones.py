from pymongo import MongoClient
import json
from pathlib import Path

# 1. Conectar a MongoDB
conn = MongoClient('mongodb+srv://paulo:Paulo2023@cluster0.prraayx.mongodb.net/BLOQUEOS_DPI?retryWrites=true&w=majority')
db = conn['BLOQUEOS_DPI']
coleccion = db['Escuelas']

# 2. Cargar el archivo padrones.json
archivo = Path(__file__).resolve().parent / 'titulares2.json'
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

# 4. Agregar los campos adicionales a cada documento
for documento in datos:
    documento['login'] = "ppaez"
    documento['empresa'] = "DPI"
    documento['activo'] = True

# 5. Insertar en MongoDB
try:
    resultado = coleccion.insert_many(datos)
    print(f"✅ Se insertaron {len(resultado.inserted_ids)} documentos en la colección 'escuelas'.")
except Exception as e:
    print(f"❌ Error al insertar: {e}")