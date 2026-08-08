# querys/usuarios.py
import json
from bson.objectid import ObjectId
from datetime import datetime
from typing import Dict, Any
# ----------------------------------------------------
from scripts.schemas.usuarios import usuariosSh
from scripts.conf.engine import get_collection
# -----------------------------------------------------


async def get_usuarios():
    coleccion = get_collection("Usuarios")
    cursor = coleccion.find()
    data = []
    async for document in cursor:
        data.append(usuariosSh(document))  # Usar esquema para transformar
    return data


async def get_usuarios_by_id(id: str):
    coleccion = get_collection("Usuarios")
    try:
        document = await coleccion.find_one({"_id": ObjectId(id)})
        if document:
            return usuariosSh(document)  # Usar esquema para transformar
        return None
    except Exception as e:
        raise Exception(f"Error al buscar documento: {e}")


async def search_usuarios_in_db(filter: Dict[str, Any]):
    coleccion = get_collection("Usuarios")
    try:
        # Filtrar eliminando valores nulos o vacíos
        query = {k: v for k, v in filter.items() if v is not None}

        # Ejecutar la búsqueda en la colección
        cursor = coleccion.find(query)
        data = []
        async for document in cursor:
            data.append(usuariosSh(document))  # Usar esquema para transformar
        return data
    except Exception as e:
        raise Exception(f"Error al buscar documentos: {e}")


async def add_usuarios(document: dict) -> ObjectId:
    coleccion = get_collection("Usuarios")
    # Inserta el documento en la colección y devuelve el ID generado
    result = await coleccion.insert_one(document)
    return result.inserted_id


async def put_usuarios(document):
    coleccion = get_collection("Usuarios")
    filtro = {"_id": ObjectId(document['id'])}
    document.pop('id')

    set_query = {"$set": document}

    respuesta = await coleccion.update_one(filtro, set_query)

    if respuesta.modified_count == 1:
        return {"status": "success", "message": "Documento actualizado correctamente"}
    else:
        return {"status": "failed", "message": "No se actualizó el documento"}


async def patch_usuarios(document: dict):
    coleccion = get_collection("Usuarios")
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
