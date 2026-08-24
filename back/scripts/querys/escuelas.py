# querys/escuelas.py
from datetime import datetime
from typing import Any, Dict

from bson.objectid import ObjectId
from scripts.conf.engine import get_collection
from scripts.schemas.escuelas import EscuelasPatch, escuelasSh


async def get_escuelas():
    coleccion = get_collection("Escuelas")
    cursor = coleccion.find()
    data = []
    async for document in cursor:
        data.append(escuelasSh(document))  # Usar esquema para transformar
    return data


async def get_escuelas_by_id(id: str):
    coleccion = get_collection("Escuelas")
    try:
        document = await coleccion.find_one({"_id": ObjectId(id)})
        if document:
            return escuelasSh(document)  # Usar esquema para transformar
        return None
    except Exception as e:
        raise Exception(f"Error al buscar documento: {e}")


async def search_escuelas_in_db(filter: Dict[str, Any]):
    coleccion = get_collection("Escuelas")
    try:
        # Filtrar eliminando valores nulos o vacíos
        query = {k: v for k, v in filter.items() if v is not None}

        # if 'mes' in query:
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
            data.append(escuelasSh(document))  # Usar esquema para transformar
        return data
    except Exception as e:
        raise Exception(f"Error al buscar documentos: {e}")


async def add_escuelas(document: dict) -> ObjectId:
    coleccion = get_collection("Escuelas")
    # Inserta el documento en la colección y devuelve el ID generado
    result = await coleccion.insert_one(document)
    return result.inserted_id


async def put_escuelas(document):
    coleccion = get_collection("Escuelas")
    filtro = {"_id": ObjectId(document["id"])}
    document.pop("id")

    set_query = {"$set": document}

    respuesta = await coleccion.update_one(filtro, set_query)

    if respuesta.modified_count == 1:
        return {"status": "success", "message": "Documento actualizado correctamente"}
    else:
        return {"status": "failed", "message": "No se actualizó el documento"}


async def patch_escuelas(document: EscuelasPatch):
    coleccion = get_collection("Escuelas")
    try:
        doc_id = document.id
        if not doc_id or not doc_id.strip():
            raise Exception("El documento debe incluir la clave 'id'")

        filtro = {"_id": ObjectId(doc_id)}

        # Solo se incluyen los campos enviados en el PATCH.
        datos = document.model_dump(exclude={"id"}, exclude_unset=True)

        if not datos:
            raise Exception("No hay campos para actualizar")

        actual = await coleccion.find_one(filtro)
        if actual is None:
            raise Exception("Documento no encontrado")

        bloqueo = datos.get("bloqueo", actual.get("bloqueo"))
        motivo = datos.get("motivo", actual.get("motivo"))

        if bloqueo is True:
            if motivo is None or not isinstance(motivo, str) or not motivo.strip():
                raise Exception("El motivo es obligatorio cuando bloqueo esta activo")

            # Todo bloqueo debe tener una fecha de baja. Se conserva la fecha
            # existente y se genera una nueva solo si todavía no existe.
            if datos.get("fecha_baja") is None:
                datos["fecha_baja"] = actual.get("fecha_baja") or datetime.now()

        elif bloqueo is False:
            datos["motivo"] = None
            datos["fecha_baja"] = None

        else:
            raise Exception("Bloqueo debe ser verdadero o falso")

        patch_query = {"$set": datos}
        respuesta = await coleccion.update_one(filtro, patch_query)

        if respuesta.modified_count == 1:
            return {
                "status": "success",
                "message": "Documento actualizado parcialmente correctamente",
            }
        else:
            return {"status": "failed", "message": "No se actualizó el documento"}
    except Exception as e:
        raise Exception(f"Error en actualización parcial: {e}")


async def get_escuelas_distinct(campo) -> list:
    coleccion = get_collection("Escuelas")
    try:
        document = await coleccion.distinct(campo, {"activo": True})
        return sorted(document)

    except Exception as e:
        raise Exception(f"Error al buscar documento: {e}")


async def search_escuelas_paginado(filter: dict, page: int = 1, page_size: int = 10):
    coleccion = get_collection("Escuelas")
    try:
        # Filtrar eliminando valores nulos o vacíos
        query = {k: v for k, v in filter.items() if v is not None}

        # Calcular el total de documentos
        total = await coleccion.count_documents(query)

        # Calcular el offset
        skip = (page - 1) * page_size

        # Ejecutar la búsqueda con paginación
        cursor = coleccion.find(query).skip(skip).limit(page_size)
        data = []
        async for document in cursor:
            data.append(escuelasSh(document))

        return {
            "data": data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }
    except Exception as e:
        raise Exception(f"Error al buscar documentos: {e}")
