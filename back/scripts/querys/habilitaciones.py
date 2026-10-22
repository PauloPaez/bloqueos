# querys/habilitaciones.py
import json
from bson.objectid import ObjectId
from datetime import datetime, timezone
from typing import Dict, Any
from zoneinfo import ZoneInfo
from datetime import datetime
# ----------------------------------------------------
from scripts.schemas.habilitaciones import habilitacionesSh
from scripts.conf.engine import get_collection
from scripts.schemas.schemaHabilitaciones import normalizar_periodo
from scripts.querys.bloqueados_historicos import guardar_bloqueados_historicos
# -----------------------------------------------------
# coleccion = database.Habilitaciones


async def get_habilitaciones():
    coleccion = get_collection("Habilitaciones")
    cursor = coleccion.find()
    data = []
    async for document in cursor:
        # Usar esquema para transformar
        data.append(habilitacionesSh(document))
    return data


async def get_habilitaciones_by_id(id: str):
    coleccion = get_collection("Habilitaciones")
    try:
        document = await coleccion.find_one({"_id": ObjectId(id)})
        if document:
            return habilitacionesSh(document)  # Usar esquema para transformar
        return None
    except Exception as e:
        raise Exception(f"Error al buscar documento: {e}")


async def search_habilitaciones_in_db(filter: Dict[str, Any]):
    coleccion = get_collection("Habilitaciones")
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
            # Usar esquema para transformar
            data.append(habilitacionesSh(document))
        return data
    except Exception as e:
        raise Exception(f"Error al buscar documentos: {e}")


async def add_habilitaciones(document: dict) -> ObjectId:
    coleccion = get_collection("Habilitaciones")
    # Inserta el documento en la colección y devuelve el ID generado
    result = await coleccion.insert_one(document)
    return result.inserted_id


async def put_habilitaciones(document):
    coleccion = get_collection("Habilitaciones")
    filtro = {"_id": ObjectId(document['id'])}
    document.pop('id')

    set_query = {"$set": document}

    respuesta = await coleccion.update_one(filtro, set_query)

    if respuesta.modified_count == 1:
        return {"status": "success", "message": "Documento actualizado correctamente"}
    else:
        return {"status": "failed", "message": "No se actualizó el documento"}


async def patch_habilitaciones(document: dict):
    coleccion = get_collection("Habilitaciones")
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


async def get_habilitaciones_distinct(campo) -> list:
    coleccion = get_collection("Habilitaciones")
    try:
        document = await coleccion.distinct(campo, {"activo": True})
        return sorted(document)

    except Exception as e:
        raise Exception(f"Error al buscar documento: {e}")


async def obtener_habilitacion_para_cierre(periodo):
    """Identifica la habilitación activa de las acreditaciones mostradas, sin cerrar durante una carga."""
    periodo = normalizar_periodo(periodo)
    if await get_collection("ControlCargas").find_one({"_id": "padrones"}):
        raise ValueError("Hay una carga en curso o pendiente de revisión. No se puede cerrar el período.")
    if not await get_collection("Escuelas").find_one({"periodo": periodo, "activo": True}, {"_id": 1}):
        raise ValueError("El período no corresponde a las acreditaciones activas cargadas.")
    documentos = await get_collection("Habilitaciones").find({"periodo": periodo, "activo": True}).to_list(length=2)
    if not documentos:
        raise ValueError(f"No hay una habilitación activa para el período {periodo}.")
    if len(documentos) > 1:
        raise ValueError(f"Hay más de una habilitación activa para {periodo}. Revise los registros antes de cerrar.")
    return documentos[0]


def estado_cierre_periodo(habilitacion):
    """Informa el plazo de cierre manual, inclusive durante todo el día límite de Argentina."""
    periodo = habilitacion["periodo"]
    fecha = habilitacion.get("fecha_cierre")
    cerrado = habilitacion.get("cerrado") is True
    hoy = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).date()
    fecha_limite = fecha.date() if fecha is not None else None
    puede_cerrar = not cerrado and fecha_limite is not None and hoy <= fecha_limite
    if cerrado:
        mensaje = f"El período {periodo} ya está cerrado."
    elif fecha_limite is None:
        mensaje = f"El período {periodo} no tiene fecha de cierre. Defínala en habilitaciones antes de cerrar."
    elif hoy > fecha_limite:
        mensaje = f"El plazo para cerrar el período {periodo} venció el {fecha_limite:%d/%m/%Y}."
    else:
        mensaje = f"Puede cerrar el período {periodo} hasta el {fecha_limite:%d/%m/%Y}, inclusive."
    return {
        "periodo": periodo, "cerrado": cerrado, "puede_cerrar": puede_cerrar,
        "fecha_limite": fecha_limite.isoformat() if fecha_limite else None, "mensaje": mensaje,
        "dias_restantes": (fecha_limite - hoy).days if fecha_limite else None,
    }


async def consultar_cierre_periodo(periodo):
    """Devuelve el plazo y cuenta las bloqueadas de todo el período, sin paginación ni filtros de pantalla."""
    habilitacion = await obtener_habilitacion_para_cierre(periodo)
    if habilitacion.get("historico_generado") is True and habilitacion.get("cerrado") is True:
        return {**estado_cierre_periodo(habilitacion), "cantidad_bloqueadas": habilitacion["cantidad_bloqueadas"]}
    cantidad = await get_collection("Escuelas").count_documents({
        "periodo": habilitacion["periodo"], "activo": True, "bloqueo": True,
    })
    return {**estado_cierre_periodo(habilitacion), "cantidad_bloqueadas": cantidad}


async def cerrar_habilitacion_periodo(periodo):
    """Guarda la copia histórica antes de confirmar el cierre manual, también cuando no hay bloqueados."""
    habilitacion = await obtener_habilitacion_para_cierre(periodo)
    estado = estado_cierre_periodo(habilitacion)
    if estado["cerrado"]:
        return estado
    if not estado["puede_cerrar"]:
        raise ValueError(estado["mensaje"])
    fecha_cierre_real = datetime.now(timezone.utc)
    cantidad = await guardar_bloqueados_historicos(habilitacion, fecha_cierre_real)
    cierre = {
        "cerrado": True, "historico_generado": True,
        "cantidad_bloqueadas": cantidad, "fecha_cierre_real": fecha_cierre_real,
    }
    resultado = await get_collection("Habilitaciones").update_one(
        {
            "_id": habilitacion["_id"], "activo": True, "cerrado": {"$ne": True},
            "fecha_cierre": habilitacion["fecha_cierre"], "periodo": habilitacion["periodo"],
        },
        {"$set": cierre},
    )
    if resultado.modified_count != 1:
        raise ValueError("La habilitación cambió durante el cierre. Actualice el listado y revise su estado.")
    return {**estado_cierre_periodo({**habilitacion, **cierre}), "cantidad_bloqueadas": cantidad}
