# querys/secuenciador.py
import json
from bson.objectid import ObjectId

# ----------------------------------------------------
# from scripts.conf.engine import database
from scripts.conf.engine import get_collection

# -----------------------------------------------------

async def get_secuencia(nombre: str):
    coleccion = get_collection("Secuencias")
    # Usar find_one_and_update asíncrono de Motor
    result = await coleccion.find_one_and_update(
        {"id": nombre}, 
        {"$inc": {"valor": 1}},
        return_document=True
    )
    
    if result:
        return result['valor']
    else:
        # Si no existe, crear nuevo documento
        nuevo_doc = {"id": nombre, "valor": 1}
        await coleccion.insert_one(nuevo_doc)
        return 1
# ----------------------------------------------------
