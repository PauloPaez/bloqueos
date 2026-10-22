from bson import ObjectId
from scripts.conf.engine import get_collection


async def guardar_bloqueados_historicos(habilitacion, fecha_cierre_real):
    """Copia los bloqueados del período; un reintento reemplaza solo la copia parcial de esta habilitación."""
    habilitacion_id = str(habilitacion["_id"])
    historicos = get_collection("BloqueadosHistoricos")
    filtro_historico = {"habilitacion_id": habilitacion_id}
    await historicos.create_index("habilitacion_id")
    bloqueados = await get_collection("Escuelas").find({
        "periodo": habilitacion["periodo"], "activo": True, "bloqueo": True,
    }).to_list(length=None)
    # El cierre llama a esta función únicamente mientras la habilitación sigue abierta.
    await historicos.delete_many(filtro_historico)
    if bloqueados:
        await historicos.insert_many([
            {
                **escuela,
                "_id": f"{habilitacion_id}:{escuela['_id']}",
                "escuela_id": str(escuela["_id"]),
                "habilitacion_id": habilitacion_id,
                "fecha_cierre_real": fecha_cierre_real,
            }
            for escuela in bloqueados
        ])
    cantidad = await historicos.count_documents(filtro_historico)
    if cantidad != len(bloqueados):
        raise RuntimeError("No se pudo verificar la cantidad de bloqueados guardados. El período no se cerró.")
    return cantidad


async def listar_periodos_historicos(page, page_size):
    """Lista cierres con histórico confirmado, incluso si no hubo bloqueados o luego se desactivó la habilitación."""
    coleccion = get_collection("Habilitaciones")
    filtro = {"cerrado": True, "historico_generado": True}
    total = await coleccion.count_documents(filtro)
    documentos = await coleccion.find(filtro).sort("fecha_cierre_real", -1).skip(
        (page - 1) * page_size
    ).limit(page_size).to_list(length=page_size)
    return {
        "data": [
            {"id": str(item["_id"]), "periodo": item["periodo"],
             "fecha_cierre_real": item["fecha_cierre_real"],
             "cantidad_bloqueadas": item["cantidad_bloqueadas"]}
            for item in documentos
        ],
        "total": total, "page": page, "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


async def consultar_bloqueados_historicos(habilitacion_id, page, page_size):
    """Devuelve la copia completa de las acreditaciones de un cierre confirmado, sin consultar Escuelas."""
    if not ObjectId.is_valid(habilitacion_id):
        raise ValueError("El ID del cierre no es válido.")
    habilitacion = await get_collection("Habilitaciones").find_one({
        "_id": ObjectId(habilitacion_id), "cerrado": True, "historico_generado": True,
    })
    if habilitacion is None:
        return None
    coleccion = get_collection("BloqueadosHistoricos")
    documentos = await coleccion.find({"habilitacion_id": str(habilitacion["_id"])}).sort(
        "_id", 1
    ).skip((page - 1) * page_size).limit(page_size).to_list(length=page_size)
    # Se conservan todos los campos de la copia; solo se adapta el identificador para la respuesta JSON.
    data = []
    for item in documentos:
        documento = dict(item)
        documento["id"] = str(documento.pop("_id"))
        data.append(documento)
    total = habilitacion["cantidad_bloqueadas"]
    return {
        "periodo": habilitacion["periodo"], "fecha_cierre_real": habilitacion["fecha_cierre_real"],
        "data": data, "total": total, "page": page, "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }
