import asyncio
import json
import re
from pathlib import Path

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


async def cargar_acreditaciones(coleccion, registros):
    """Inserta directamente en Escuelas por lotes y verifica la cantidad cargada."""
    for inicio in range(0, len(registros), TAMANO_LOTE):
        await coleccion.insert_many(registros[inicio:inicio + TAMANO_LOTE], ordered=True)
    cantidad = await coleccion.count_documents({})
    if cantidad != len(registros):
        raise RuntimeError(f"Carga incompleta: se esperaban {len(registros)} registros y hay {cantidad}.")


async def validar_periodo_nuevo(base, periodo):
    """Rechaza períodos iguales o anteriores al último registrado en habilitaciones activas."""
    periodos = await base["Habilitaciones"].distinct("periodo", {"activo": True})
    # Una carga parcial en Escuelas no es una habilitación completada y debe poder reintentarse.
    # Los documentos sin período no definen un mes contra el cual comparar la carga.
    periodos = [valor for valor in periodos if valor is not None and valor != ""]
    if periodos:
        ultimo = max(periodos, key=ordenar_periodo)
        if ordenar_periodo(periodo) <= ordenar_periodo(ultimo):
            raise ValueError(f"El período {periodo} debe ser posterior al último período: {ultimo}.")


async def importar_padron(periodo: str, directorio: Path = DIRECTORIO_JSON) -> dict:
    """Valida el JSON y reemplaza los documentos; el coordinador controla la reserva y el cierre."""
    # La lectura del JSON no bloquea el procesamiento de otras solicitudes del backend.
    registros = await asyncio.to_thread(leer_padron, periodo, directorio)
    periodo = periodo.upper()
    coleccion = get_collection("Escuelas")
    await validar_periodo_nuevo(coleccion.database, periodo)

    # El JSON completo ya está validado. Vaciar documentos conserva los índices y opciones.
    # Si falla la inserción, Escuelas puede quedar parcial; el reintento vuelve a vaciarla.
    await coleccion.delete_many({})
    await cargar_acreditaciones(coleccion, registros)

    return {"periodo": periodo, "cantidad": len(registros)}
