# querys/rutas.py
import json
from bson.objectid import ObjectId
from datetime import datetime
from typing import Dict, Any 
# ----------------------------------------------------
from scripts.schemas.rutas import rutasSh
# from scripts.conf.engine import database
from scripts.conf.engine import get_collection
# -----------------------------------------------------
# coleccion = database.Rutas

async def get_rutas():
    coleccion = get_collection("Rutas")
    cursor = coleccion.find()
    data = []
    async for document in cursor:
        data.append(rutasSh(document))  # Usar esquema para transformar
    return data
    
  
async def get_rutas_by_id(id: str):
    coleccion = get_collection("Rutas")
    try:
        document = await coleccion.find_one({"_id": ObjectId(id)})
        if document:
            return rutasSh(document)  # Usar esquema para transformar
        return None
    except Exception as e:
        raise Exception(f"Error al buscar documento: {e}")
    
async def search_rutas_in_db(filter: Dict[str, Any]):
    coleccion = get_collection("Rutas")
    try:
        # Filtrar eliminando valores nulos o vacíos
        query = {k: v for k, v in filter.items() if v is not None}
        
        # Ejecutar la búsqueda en la colección
        cursor = coleccion.find(query)
        data = []
        async for document in cursor:
            data.append(rutasSh(document))  # Usar esquema para transformar
        return data
    except Exception as e:
        raise Exception(f"Error al buscar documentos: {e}")    
 
async def add_rutas(document: dict) -> ObjectId:
    coleccion = get_collection("Rutas")
    # Inserta el documento en la colección y devuelve el ID generado
    result = await coleccion.insert_one(document)
    return result.inserted_id

async def put_rutas(document):
    coleccion = get_collection("Rutas")
    filtro = {"_id": ObjectId(document['id'])}
    document.pop('id')

    set_query = {"$set": document}

    respuesta = await coleccion.update_one(filtro, set_query)

    if respuesta.modified_count == 1:
        return {"status": "success", "message": "Documento actualizado correctamente"}
    else:
        return {"status": "failed", "message": "No se actualizó el documento"}
