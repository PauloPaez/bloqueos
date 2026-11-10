import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, time, timezone
from typing import Any, Dict
from zoneinfo import ZoneInfo

from bson.objectid import ObjectId
from scripts.conf.engine import get_collection
from scripts.querys.bloqueados_historicos import guardar_bloqueados_historicos
from scripts.schemas.habilitaciones import habilitacionesSh
from scripts.schemas.schemaHabilitaciones import normalizar_periodo
from utils.generacionTXT import generar_txt_por_archivo
from utils.padrones.archivosCierre import (
    descartar_txt_cierre,
    guardar_txt_cierre,
)


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


async def habilitacion_esta_cerrada(id) -> bool:
    documento = await get_collection("Habilitaciones").find_one({"_id": ObjectId(id), "cerrado": True}, {"_id": 1})
    return documento is not None


# Vive en memoria: si el proceso se corta, desaparece y se puede reintentar. Requiere un solo proceso.
candado_padrones = asyncio.Lock()


@asynccontextmanager
async def reservar_padrones():
    """Impide operaciones simultáneas de carga, cierre o reapertura."""
    if candado_padrones.locked():
        raise ValueError("Hay una carga, cierre o reapertura en curso. Intente más tarde.")
    async with candado_padrones:
        yield


async def reabrir_habilitacion(id):
    """Descarta los TXT y el histórico, y abre el período. Si falla, sigue cerrado y se puede reintentar."""
    if not ObjectId.is_valid(id):
        raise ValueError("El ID de la habilitación no es válido.")
    coleccion = get_collection("Habilitaciones")
    async with reservar_padrones():
        habilitacion = await coleccion.find_one({"_id": ObjectId(id), "activo": True, "cerrado": True})
        if habilitacion is None:
            raise ValueError("No se encontró una habilitación activa y cerrada para reabrir.")
        periodo = habilitacion["periodo"]
        # Escuelas contiene un solo período: si no es este, sus datos ya no se pueden volver a cerrar.
        if not await get_collection("Escuelas").find_one({"periodo": periodo, "activo": True}, {"_id": 1}):
            raise ValueError(f"No se puede reabrir {periodo} porque sus acreditaciones ya no están cargadas.")
        # La habilitación se abre al final: así un fallo intermedio se resuelve reintentando.
        descartar_txt_cierre(periodo)
        await get_collection("BloqueadosHistoricos").delete_many({"habilitacion_id": str(habilitacion["_id"])})
        await coleccion.update_one(
            {"_id": habilitacion["_id"]},
            {"$set": {"cerrado": False},
             "$unset": {"historico_generado": "", "cantidad_bloqueadas": "", "fecha_cierre_real": ""}},
        )
    return {"id": str(habilitacion["_id"]), "periodo": periodo, "cerrado": False,
            "message": "Período reabierto. Actualice la fecha de cierre antes de editar."}


async def obtener_habilitacion_para_cierre(periodo):
    """Identifica la habilitación activa de las acreditaciones mostradas."""
    periodo = normalizar_periodo(periodo)
    if not await get_collection("Escuelas").find_one({"periodo": periodo, "activo": True}, {"_id": 1}):
        raise ValueError("El período no corresponde a las acreditaciones activas cargadas.")
    documentos = await get_collection("Habilitaciones").find({"periodo": periodo, "activo": True}).to_list(length=2)
    if not documentos:
        raise ValueError(f"No hay una habilitación activa para el período {periodo}.")
    if len(documentos) > 1:
        raise ValueError(f"Hay más de una habilitación activa para {periodo}. Revise los registros antes de cerrar.")
    return documentos[0]


def estado_cierre_periodo(habilitacion):
    """Informa el plazo de cierre manual usando fecha y hora de Argentina."""
    periodo = habilitacion["periodo"]
    fecha = habilitacion.get("fecha_cierre")
    hora = habilitacion.get("hora_cierre")
    cerrado = habilitacion.get("cerrado") is True
    zona = ZoneInfo("America/Argentina/Buenos_Aires")
    ahora = datetime.now(zona)
    fecha_limite = fecha.date() if fecha is not None else None
    hora_limite = time.fromisoformat(hora) if hora else time.max
    vencimiento = datetime.combine(fecha_limite, hora_limite, tzinfo=zona) if fecha_limite else None
    vencido = vencimiento is not None and ahora > vencimiento
    segundos_restantes = max(0, int((vencimiento - ahora).total_seconds())) if vencimiento else None
    puede_cerrar = not cerrado and vencimiento is not None
    puede_editar = puede_cerrar and not vencido
    if cerrado:
        mensaje = f"El período {periodo} fue cerrado con éxito."
    elif fecha_limite is None:
        mensaje = f"El período {periodo} no tiene fecha de cierre. Defínala en habilitaciones antes de cerrar."
    elif ahora > vencimiento:
        detalle_limite = f"{fecha_limite:%d/%m/%Y} a las {hora}" if hora else f"{fecha_limite:%d/%m/%Y} (fin del día)"
        mensaje = f"El plazo para editar el período {periodo} venció el {detalle_limite}. Puede cerrar el período."
    else:
        detalle_limite = f"{fecha_limite:%d/%m/%Y} a las {hora}" if hora else f"{fecha_limite:%d/%m/%Y}, inclusive"
        mensaje = f"Puede cerrar el período {periodo} hasta el {detalle_limite}."
    return {
        "periodo": periodo, "cerrado": cerrado, "puede_cerrar": puede_cerrar,
        "puede_editar": puede_editar,
        "fecha_limite": fecha_limite.isoformat() if fecha_limite else None, "mensaje": mensaje,
        "hora_limite": hora, "vencido": vencido, "segundos_restantes": segundos_restantes,
        "dias_restantes": (fecha_limite - ahora.date()).days if fecha_limite else None,
    }


async def consultar_cierre_periodo(periodo):
    """Devuelve el plazo y cuenta las bloqueadas de todo el período, sin paginación ni filtros de pantalla."""
    if candado_padrones.locked():
        raise ValueError("Hay una carga, cierre o reapertura en curso. Intente más tarde.")
    habilitacion = await obtener_habilitacion_para_cierre(periodo)
    if habilitacion.get("historico_generado") is True and habilitacion.get("cerrado") is True:
        return {**estado_cierre_periodo(habilitacion), "cantidad_bloqueadas": habilitacion["cantidad_bloqueadas"]}
    cantidad = await get_collection("Escuelas").count_documents({
        "periodo": habilitacion["periodo"], "activo": True, "bloqueo": True,
    })
    return {**estado_cierre_periodo(habilitacion), "cantidad_bloqueadas": cantidad}


async def cerrar_habilitacion_periodo(periodo):
    """Publica los TXT y guarda el histórico; marca cerrado al final. Si falla, sigue abierto y se puede reintentar."""
    async with reservar_padrones():
        habilitacion = await obtener_habilitacion_para_cierre(periodo)
        estado = estado_cierre_periodo(habilitacion)
        if estado["cerrado"]:
            return estado
        if not estado["puede_cerrar"]:
            raise ValueError(estado["mensaje"])
        bloqueados = await get_collection("Escuelas").find({
            "periodo": habilitacion["periodo"], "activo": True, "bloqueo": True,
        }).to_list(length=None)
        archivos = generar_txt_por_archivo(bloqueados, habilitacion["periodo"])
        fecha_cierre_real = datetime.now(timezone.utc)
        # El destino activo (SFTP, con respaldo local) está definido en archivosCierre.py.
        # Si falla el histórico o el cierre, el contexto elimina solo sus propios TXT.
        with guardar_txt_cierre(habilitacion["periodo"], archivos) as rutas:
            cantidad = await guardar_bloqueados_historicos(habilitacion, fecha_cierre_real, bloqueados)
            cierre = {
                "cerrado": True, "historico_generado": True,
                "cantidad_bloqueadas": cantidad, "fecha_cierre_real": fecha_cierre_real,
            }
            await get_collection("Habilitaciones").update_one({"_id": habilitacion["_id"]}, {"$set": cierre})
    return {**estado_cierre_periodo({**habilitacion, **cierre}),
            "cantidad_bloqueadas": cantidad, "archivos_generados": rutas}
