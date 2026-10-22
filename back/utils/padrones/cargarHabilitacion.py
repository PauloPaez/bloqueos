import asyncio
from datetime import datetime, timezone

from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from scripts.conf.engine import get_collection
from scripts.querys.habilitaciones import add_habilitaciones
from utils.padrones.descargarPadrones import DIR_LOCAL, descargar_archivos, variables_ambiente
from utils.padrones.prefijos import es_archivo_padron
from utils.padrones.generar_padron_json import DESTINO, generar_padron_json
from utils.padrones.importPadron import (
    importar_padron,
    ordenar_periodo,
    validar_periodo_nuevo,
)


async def verificar_cierre_anterior(base):
    """Exige el cierre manual del último período activo registrado; la fecha no lo cierra."""
    anteriores = [
        item async for item in base["Habilitaciones"].find({"activo": True})
        if item.get("periodo") not in (None, "")
    ]
    if anteriores:
        ultimo = max(ordenar_periodo(item["periodo"]) for item in anteriores)
        for item in anteriores:
            if ordenar_periodo(item["periodo"]) == ultimo and item.get("cerrado") is not True:
                raise ValueError(f"Debe cerrar manualmente el período {item['periodo']} antes de cargar otro.")


def preparar_archivos(documento):
    """Descarga por SFTP y genera el JSON en un hilo, sin escrituras en el servidor de origen."""
    host, usuario, clave, remoto = variables_ambiente()
    archivos = descargar_archivos(host, usuario, clave, remoto, documento["periodo"])
    if not archivos:
        raise ValueError("No hay archivos SUAC/TIAC con datos para cargar.")
    generar_padron_json(
        documento["periodo"], login=documento.get("login"), empresa=documento.get("empresa"),
    )


def limpiar_archivos_procesados(periodo):
    """Borra únicamente las fuentes y el JSON locales del período ya cargado y registrado."""
    ordenar_periodo(periodo)
    periodo = periodo.upper()
    archivos = [
        archivo for archivo in DIR_LOCAL.iterdir()
        if archivo.is_file() and es_archivo_padron(archivo.name, periodo)
    ] if DIR_LOCAL.exists() else []
    archivos.append(DESTINO / f"{periodo}.json")
    for archivo in archivos:
        try:
            archivo.unlink(missing_ok=True)
        except OSError as error:
            # Un archivo que no se pudo borrar no impide limpiar los restantes.
            print(f"ERROR al eliminar el archivo procesado {archivo}: {error}")


async def crear_habilitacion_con_padron(documento):
    """Ejecuta los tres procesos y registra la habilitación solo después de completarse la carga."""
    base = get_collection("Habilitaciones").database
    control = base["ControlCargas"]
    documento = {**documento, "_id": ObjectId(), "cerrado": False, "activo": True}
    # El _id fijo impide cargas simultáneas entre workers. Sin TTL: no vence durante una carga lenta.
    reserva = {
        "_id": "padrones", "inicio": datetime.now(timezone.utc), "habilitacion": documento,
    }
    try:
        await control.insert_one(reserva)
    except DuplicateKeyError:
        raise ValueError("Hay una carga en curso o pendiente de revisión. No inicie otra carga.")

    etapa = "validar el período y su cierre"
    importacion_iniciada = False
    importado = False
    try:
        await validar_periodo_nuevo(base, documento["periodo"])
        await verificar_cierre_anterior(base)
        etapa = "descargar los archivos y generar el JSON"
        # shield evita liberar la reserva mientras un hilo sigue escribiendo tras una desconexión.
        preparacion = asyncio.create_task(asyncio.to_thread(preparar_archivos, documento))
        await asyncio.shield(preparacion)
        etapa = "importar las acreditaciones"
        importacion_iniciada = True
        resultado = await importar_padron(documento["periodo"])
        importado = True
        etapa = "registrar la habilitación"
        try:
            await add_habilitaciones(documento)
        except Exception:
            # Un error de red puede llegar después de que insert_one haya sido aplicado.
            if await base["Habilitaciones"].find_one({"_id": documento["_id"]}) is None:
                raise
    except Exception as error:
        print(f"ERROR al {etapa}: {error}")
        if not importacion_iniciada:
            await control.delete_one({"_id": "padrones", "habilitacion._id": documento["_id"]})
            if etapa == "validar el período y su cierre" and isinstance(error, ValueError):
                raise
        # Tras iniciar la importación se conserva la reserva para revisar un posible cambio en Escuelas.
        # También queda reservada ante una cancelación: el hilo podría continuar trabajando.
        if importado:
            raise RuntimeError(
                "Las acreditaciones se cargaron, pero no se pudo confirmar el registro de la habilitación. "
                "No repita la carga: revise Habilitaciones y ControlCargas."
            ) from error
        raise RuntimeError(
            f"No se pudo completar la carga al {etapa}. "
            + ("Escuelas puede contener una carga parcial. Revise Escuelas y ControlCargas antes de reintentar." if importacion_iniciada else "No se importaron acreditaciones.")
        ) from error

    # Limpiamos solo después del guardado confirmado y todavía con la reserva tomada.
    # Una limpieza fallida no convierte una carga completada en un error para el usuario.
    try:
        await asyncio.to_thread(limpiar_archivos_procesados, documento["periodo"])
    except Exception as error:
        print(f"ERROR al limpiar los archivos de la carga completada: {error}")

    # El guardado ya terminó: un fallo al liberar la reserva tampoco invalida la carga.
    try:
        await control.delete_one({"_id": "padrones", "habilitacion._id": documento["_id"]})
    except Exception as error:
        print(f"ERROR al liberar ControlCargas después de guardar la habilitación: {error}")
    return {"id": str(documento["_id"]), "periodo": documento["periodo"], "cantidad": resultado["cantidad"]}
