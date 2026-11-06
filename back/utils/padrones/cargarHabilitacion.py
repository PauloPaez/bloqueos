import asyncio

from bson import ObjectId
from scripts.conf.engine import get_collection
from scripts.querys.habilitaciones import add_habilitaciones, reservar_padrones
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
    """Carga las acreditaciones y registra la habilitación al final. Si falla, no queda registrada y se puede reintentar."""
    base = get_collection("Habilitaciones").database
    documento = {**documento, "_id": ObjectId(), "cerrado": False, "activo": True}
    async with reservar_padrones():
        await validar_periodo_nuevo(base, documento["periodo"])
        await verificar_cierre_anterior(base)
        etapa = "descargar los archivos y generar el JSON"
        try:
            await asyncio.to_thread(preparar_archivos, documento)
            etapa = "importar las acreditaciones"
            resultado = await importar_padron(documento["periodo"])
            etapa = "registrar la habilitación"
            try:
                await add_habilitaciones(documento)
            except Exception:
                # Un error de red puede llegar después de que insert_one haya sido aplicado.
                if await base["Habilitaciones"].find_one({"_id": documento["_id"]}) is None:
                    raise
        except Exception as error:
            print(f"ERROR al {etapa}: {error}")
            raise RuntimeError(f"No se pudo completar la carga al {etapa}. Reintente la operación.") from error

        # Limpiamos solo después del guardado confirmado y todavía con la reserva tomada.
        # Una limpieza fallida no convierte una carga completada en un error para el usuario.
        try:
            await asyncio.to_thread(limpiar_archivos_procesados, documento["periodo"])
        except Exception as error:
            print(f"ERROR al limpiar los archivos de la carga completada: {error}")
    return {"id": str(documento["_id"]), "periodo": documento["periodo"], "cantidad": resultado["cantidad"]}
