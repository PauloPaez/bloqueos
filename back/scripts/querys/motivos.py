# querys/motivos.py
import json
from datetime import datetime
from typing import Any, Dict

from bson.objectid import ObjectId
from scripts.conf.engine import get_collection
from scripts.schemas.motivos import motivosSh


async def get_motivos():
    coleccion = get_collection("Motivos")
    cursor = coleccion.find()
    data = []
    async for document in cursor:
        data.append(motivosSh(document))  # Usar esquema para transformar
    return data
  
async def get_motivos_by_id(id: str):
    coleccion = get_collection("Motivos")
    try:
        document = await coleccion.find_one({"_id": ObjectId(id)})
        if document:
            return motivosSh(document)  # Usar esquema para transformar
        return None
    except Exception as e:
        raise Exception(f"Error al buscar documento: {e}")
    
async def search_motivos_in_db(filter: Dict[str, Any]):
    coleccion = get_collection("Motivos")
    try:
        # Filtrar eliminando valores nulos o vacíos
        query = {k: v for k, v in filter.items() if v is not None}
        
        #if 'mes' in query:
        #    mes= query['mes']
        #    del query['mes']
        #    query['fecha_accidente'] = {
        #        "$gte": datetime(2025, mes, 1),
        #        "$lt": datetime(2025, mes + 1, 1)
        #    }

        # Ejecutar la búsqueda en la colección
        cursor = coleccion.find(query)
        data = []
        async for document in cursor:
            data.append(motivosSh(document))  # Usar esquema para transformar
        return data
    except Exception as e:
        raise Exception(f"Error al buscar documentos: {e}")    
 
async def add_motivos(document: dict) -> ObjectId:
    coleccion = get_collection("Motivos")
    # Inserta el documento en la colección y devuelve el ID generado
    result = await coleccion.insert_one(document)
    return result.inserted_id

async def put_motivos(document):
    coleccion = get_collection("Motivos")
    filtro = {"_id": ObjectId(document['id'])}
    document.pop('id')

    set_query = {"$set": document}

    respuesta = await coleccion.update_one(filtro, set_query)

    if respuesta.modified_count == 1:
        return {"status": "success", "message": "Documento actualizado correctamente"}
    else:
        return {"status": "failed", "message": "No se actualizó el documento"}

async def patch_motivos(document: dict):
    coleccion = get_collection("Motivos")
    try:
        # Se espera que el diccionario incluya la clave "id" para identificar el documento
        doc_id = document.get("id")
        if not doc_id:
            raise Exception("El documento debe incluir la clave 'id'")
        
        filtro = {"_id": ObjectId(doc_id)}
        document.pop("id")
        
        patch_query = {"$set": document}
        respuesta = await coleccion.update_one(filtro, patch_query)
        
        if respuesta.modified_count == 1:
            return {"status": "success", "message": "Documento actualizado parcialmente correctamente"}
        else:
            return {"status": "failed", "message": "No se actualizó el documento"}
    except Exception as e:
        raise Exception(f"Error en actualización parcial: {e}")

async def get_motivos_distinct(campo) -> list:
    coleccion = get_collection("Motivos")
    try:
        document = await coleccion.distinct(campo, {"activo": True})
        return sorted(document) 

    except Exception as e:
        raise Exception(f"Error al buscar documento: {e}")
