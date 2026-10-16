import asyncio
import json
import re
from pathlib import Path

from pymongo import IndexModel
from scripts.conf.engine import get_collection

DIRECTORIO_JSON = Path(__file__).resolve().parents[3] / "datos" / "fuentes_formateadas"
TAMANO_LOTE = 10000


def ordenar_periodo(periodo: str) -> tuple[int, int]:
    """Convierte MESAA en año y mes para comparar períodos cronológicamente."""
    if not isinstance(periodo, str):
        raise ValueError(f"Período inválido: {periodo}. Se espera texto con formato MESAA.")
    meses = [
        "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
        "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE",
    ]
    coincidencia = re.fullmatch(r"([A-Z]+)([0-9]{2})", periodo.upper())
    if not coincidencia:
        raise ValueError(f"Período inválido: {periodo}. Se espera un mes y dos dígitos de año.")
    mes, anio = coincidencia.groups()
    mes = "SETIEMBRE" if mes == "SEPTIEMBRE" else mes
    if mes not in meses:
        raise ValueError(f"Mes desconocido en el período: {periodo}.")
    return int(anio), meses.index(mes) + 1


def leer_padron(periodo: str, directorio: Path = DIRECTORIO_JSON) -> list[dict]:
    """Valida el archivo completo antes de realizar cualquier escritura en MongoDB."""
    if not periodo or not periodo.isascii() or not periodo.isalnum():
        raise ValueError("El período debe contener solamente letras y números ASCII.")
    ordenar_periodo(periodo)
    periodo = periodo.upper()
    archivo = directorio / f"{periodo}.json"
    with archivo.open(encoding="utf-8") as entrada:
        registros = json.load(entrada)
    if not isinstance(registros, list) or not registros:
        raise ValueError("El JSON debe contener una lista de acreditaciones no vacía.")
    for numero, registro in enumerate(registros, start=1):
        if not isinstance(registro, dict) or registro.get("periodo") != periodo:
            raise ValueError(f"Registro {numero}: no corresponde al período {periodo}.")
    return registros


async def copiar_indices(actual, temporal):
    """Prepara en la nueva colección los índices existentes, salvo el _id automático."""
    indices = []
    async for indice in actual.list_indexes():
        if indice["name"] == "_id_":
            continue
        opciones = {k: v for k, v in indice.items() if k not in {"key", "v", "ns"}}
        indices.append(IndexModel(list(indice["key"].items()), **opciones))
    if indices:
        await temporal.create_indexes(indices)


async def cargar_temporal(temporal, registros):
    """Inserta por lotes y verifica la cantidad sin modificar las acreditaciones vigentes."""
    for inicio in range(0, len(registros), TAMANO_LOTE):
        await temporal.insert_many(registros[inicio:inicio + TAMANO_LOTE], ordered=True)
    cantidad = await temporal.count_documents({})
    if cantidad != len(registros):
        raise RuntimeError(f"Carga incompleta: se esperaban {len(registros)} registros y hay {cantidad}.")


async def validar_periodo_nuevo(base, periodo): #aca verifica tambien los periodos en la base de datos de habilitaciones y los de Escuelas/acreditaciones
    """Rechaza períodos iguales o anteriores al último registrado o importado activo."""
    periodos = await base["Habilitaciones"].distinct("periodo", {"activo": True})
    # Escuelas también protege frente a una importación cuyo registro en el historial falló.
    periodos += await base["Escuelas"].distinct("periodo", {"activo": True})
    # Los documentos sin período no definen un mes contra el cual comparar la carga.
    periodos = [valor for valor in periodos if valor is not None and valor != ""]
    if periodos:
        ultimo = max(periodos, key=ordenar_periodo)
        if ordenar_periodo(periodo) <= ordenar_periodo(ultimo):
            raise ValueError(f"El período {periodo} debe ser posterior al último período: {ultimo}.")


async def importar_padron(periodo: str, directorio: Path = DIRECTORIO_JSON) -> dict:
    """Coordina validación, carga temporal y reemplazo usando la conexión del backend."""
    # La lectura del JSON no bloquea el procesamiento de otras solicitudes del backend.
    registros = await asyncio.to_thread(leer_padron, periodo, directorio)
    periodo = periodo.upper()
    actual = get_collection("Escuelas")
    base = actual.database
    nombres = await base.list_collection_names()
    if "EscuelasTemporal" in nombres:
        raise RuntimeError("Existe EscuelasTemporal: hay una carga en curso o pendiente de revisión.")
    existe_actual = "Escuelas" in nombres

    # Crear con el nombre fijo también impide que dos importadores lo reserven a la vez.
    # Si el servidor rechaza la creación, no borramos la temporal de otro proceso.
    opciones = await actual.options() if existe_actual else {}
    temporal = await base.create_collection("EscuelasTemporal", check_exists=False, **opciones)
    publicacion_iniciada = False
    try:
        # Se valida después de reservar la temporal para evitar dos cargas concurrentes.
        await validar_periodo_nuevo(base, periodo)
        if existe_actual:
            await copiar_indices(actual, temporal)
        await cargar_temporal(temporal, registros)
        publicacion_iniciada = True
        # Sustituye Escuelas en una sola operación del servidor, sin respaldo completo.
        # El cierre del período y su histórico de bloqueados se integrarán en el flujo de habilitaciones.
        try:
            await temporal.rename("Escuelas", dropTarget=True)
        except Exception as error:
            # Si se perdió la respuesta de red, la operación podría haberse completado.
            # No borramos nada ni reintentamos automáticamente: requiere revisar el estado.
            raise RuntimeError(
                "No se pudo confirmar la publicación. Revisar Escuelas y EscuelasTemporal antes de reintentar."
            ) from error
    except Exception:
        if not publicacion_iniciada:
            # Una carga parcial se descarta; Escuelas permanece intacta.
            await temporal.drop()
        # Tras iniciar el renombrado conservamos los datos disponibles para inspección.
        raise

    return {"periodo": periodo, "cantidad": len(registros)}
