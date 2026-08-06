# querys/personas.py
from bson.objectid import ObjectId
from datetime import datetime
from typing import Dict, Any 
from datetime import datetime
# ----------------------------------------------------
from scripts.schemas.personas import personasSh
from scripts.conf.engine import get_collection
# -----------------------------------------------------

async def get_personas():
    coleccion = get_collection("Personas")
    cursor = coleccion.find()
    data = []
    async for document in cursor:
        data.append(personasSh(document))  # Usar esquema para transformar
    return data
  
async def get_personas_by_id(id: str):
    coleccion = get_collection("Personas")
    try:
        document = await coleccion.find_one({"_id": ObjectId(id)})
        if document:
            return personasSh(document)  # Usar esquema para transformar
        return None
    except Exception as e:
        raise Exception(f"Error al buscar documento: {e}")
    
async def search_personas_in_db(filter: Dict[str, Any]):
    coleccion = get_collection("Personas")
    try:
        # Filtrar eliminando valores nulos o vacíos
        query = {k: v for k, v in filter.items() if v is not None}
     
        # Ejecutar la búsqueda en la colección
        cursor = coleccion.find(query)
        data = []
        async for document in cursor:
            data.append(personasSh(document))  # Usar esquema para transformar
        return data
    except Exception as e:
        raise Exception(f"Error al buscar documentos: {e}")    
 
async def add_personas(document: dict) -> ObjectId:
    coleccion = get_collection("Personas")
    # Inserta el documento en la colección y devuelve el ID generado
    result = await coleccion.insert_one(document)
    return result.inserted_id

async def put_personas(document):
    coleccion = get_collection("Personas")
    filtro = {"_id": ObjectId(document['id'])}
    document.pop('id')

    set_query = {"$set": document}

    respuesta = await coleccion.update_one(filtro, set_query)

    if respuesta.matched_count != 1:
        return {"status": "failed", "message": "No se encontró el documento"}
    if respuesta.modified_count == 1:
        return {"status": "success", "message": "Documento actualizado correctamente"}
    return {"status": "success", "message": "Documento sin cambios"}

async def patch_personas(document: dict):
    coleccion = get_collection("Personas")
    try:
        # Se espera que el diccionario incluya la clave "id" para identificar el documento
        doc_id = document.get("id")
        if not doc_id:
            raise Exception("El documento debe incluir la clave 'id'")
        
        filtro = {"_id": ObjectId(doc_id)}
        document.pop("id")
        
        patch_query = {"$set": document}
        respuesta = await coleccion.update_one(filtro, patch_query)
        
        if respuesta.matched_count != 1:
            return {"status": "failed", "message": "No se encontró el documento"}
        if respuesta.modified_count == 1:
            return {"status": "success", "message": "Documento actualizado parcialmente correctamente"}
        return {"status": "success", "message": "Documento sin cambios"}
    except Exception as e:
        raise Exception(f"Error en actualización parcial: {e}")

async def get_personas_distinct(campo) -> list:
    try:
        document = await coleccion.distinct(campo, {"activo": True})
        return sorted(document) 

    except Exception as e:
        raise Exception(f"Error al buscar documento: {e}")
