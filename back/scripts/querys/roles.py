# querys/roles.py
import json
from bson.objectid import ObjectId
from datetime import datetime
from typing import Dict, Any 
# ----------------------------------------------------
from scripts.schemas.roles import rolesSh
from scripts.conf.engine import database
# -----------------------------------------------------
coleccion = database.Roles

async def get_roles():
    cursor = coleccion.find()
    data = []
    async for document in cursor:
        data.append(rolesSh(document))  # Usar esquema para transformar
    return data
    
  
async def get_roles_by_id(id: str):
    try:
        document = await coleccion.find_one({"_id": ObjectId(id)})
        if document:
            return rolesSh(document)  # Usar esquema para transformar
        return None
    except Exception as e:
        raise Exception(f"Error al buscar documento: {e}")
    
async def search_roles_in_db(filter: Dict[str, Any]):
    try:
        # Filtrar eliminando valores nulos o vacíos
        query = {k: v for k, v in filter.items() if v is not None}
        
        # Ejecutar la búsqueda en la colección
        cursor = coleccion.find(query)
        data = []
        async for document in cursor:
            data.append(rolesSh(document))  # Usar esquema para transformar
        return data
    except Exception as e:
        raise Exception(f"Error al buscar documentos: {e}")    
 
async def add_roles(document: dict) -> ObjectId:
    # Inserta el documento en la colección y devuelve el ID generado
    result = await coleccion.insert_one(document)
    return result.inserted_id

async def put_roles(document):
    filtro = {"_id": ObjectId(document['id'])}
    document.pop('id')

    set_query = {"$set": document}

    respuesta = await coleccion.update_one(filtro, set_query)

    if respuesta.modified_count == 1:
        return {"status": "success", "message": "Documento actualizado correctamente"}
    else:
        return {"status": "failed", "message": "No se actualizó el documento"}
