import re
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import Any


def formatear_importe(valor: str | int | float | Decimal | None) -> str:
    """Formatea un importe usando la misma regla que la planilla de bajas."""
    if valor is None or valor == "":
        return ""

    importe = Decimal(str(valor)) / Decimal("100")
    parte_entera, parte_decimal = f"{importe:.2f}".split(".")
    parte_entera_formateada = f"{int(parte_entera):,}".replace(",", ".")
    return f"{parte_entera_formateada},{parte_decimal}"


def formatear_cuil(cuil: str) -> str:
    return f"{cuil[:2]}-{cuil[2:10]}-{cuil[10]}"


_MESES = {
    "ENERO": "01",
    "FEBRERO": "02",
    "MARZO": "03",
    "ABRIL": "04",
    "MAYO": "05",
    "JUNIO": "06",
    "JULIO": "07",
    "AGOSTO": "08",
    "SEPTIEMBRE": "09",
    "SETIEMBRE": "09",
    "OCTUBRE": "10",
    "NOVIEMBRE": "11",
    "DICIEMBRE": "12",
}


def formatear_periodo(periodo: Any) -> str:
    """Convierte periodos como JUNIO26 en 06-2026."""
    valor = _texto(periodo).strip().upper()
    if not valor:
        return ""

    periodo_numerico = re.fullmatch(r"(\d{1,2})[-/]?(20\d{2})", valor)
    if periodo_numerico:
        mes, anio = periodo_numerico.groups()
        return f"{mes.zfill(2)}-{anio}"

    periodo_nombre = re.fullmatch(r"([A-ZÁÉÍÓÚ]+)(\d{2})", valor)
    if periodo_nombre:
        nombre_mes, anio = periodo_nombre.groups()
        mes = _MESES.get(nombre_mes)
        if mes:
            return f"{mes}-20{anio}"

    return valor

#TODO: Falta agregar logica al tipo de banco
def formatear_concepto(
    tipo_archivo: Any,
    periodo: Any,
    tipo_banco: str = "tipo_banco",
) -> str:
    """Construye el concepto visible para tablas y documentos."""
    archivo = _texto(tipo_archivo).strip()
    periodo_formateado = formatear_periodo(periodo)
    banco = _texto(tipo_banco).strip()

    if not archivo or not periodo_formateado or not banco:
        return ""

    return f"{archivo}.{periodo_formateado}.{banco}"


def _texto(valor: Any) -> str:
    return "" if valor is None else str(valor)


def _con_digito_verificador(valor: Any, digito: Any) -> str: #formatear padron
    base = _texto(valor)
    dv = _texto(digito)
    if not base:
        return dv
    return f"{base}/{dv}" if dv else base


def _valores_de_fila(escuela: Any) -> Mapping[str, Any]:
    """Obtiene los valores tanto de un modelo Pydantic como de un dict."""
    if isinstance(escuela, Mapping):
        return escuela
    if hasattr(escuela, "model_dump"):
        return escuela.model_dump()
    return vars(escuela)


def formatear_motivo_fecha_baja(
    motivo: str | None,
    fecha_baja: datetime | None,
    motivos_config: Mapping[str, bool] | None = None,
) -> str:
    motivo_configurado = motivos_config or {}
    lleva_fecha = motivo_configurado.get(_texto(motivo).strip().casefold(), False)
    if motivo and fecha_baja and lleva_fecha:
        return f"{motivo} ({fecha_baja.date()})"
    return _texto(motivo)
#TODO: ver si agregar upper o no al formatear. Quiza lo deje asi y que en la base de datos se guarden en mayus
#TODO: Nota: con fontSize 10 en word, entran todas las fechas. Obviamente habiendo movido el tamaño que ocupa cada columna

def preparar_fila_baja(
    escuela: Any,
    motivos_config: Mapping[str, bool] | None = None,
) -> dict[str, str]:
    """Construye los valores visibles de una fila de Excel/Word.

    Esta es la única definición de formato para las columnas compartidas por
    ambos documentos. El template recibe únicamente strings ya preparados.
    """
    row = _valores_de_fila(escuela)
    cuil = _texto(row.get("cuil")).strip()

    return {
        "concepto": formatear_concepto(
            row.get("tipo_archivo"), row.get("periodo")
        ),
        "padron": _con_digito_verificador(row.get("padron"), row.get("padron_dv")),
        "beneficiario_nombre": _texto(row.get("beneficiario_nombre")),
        "importe": formatear_importe(row.get("importe_acreditado")),
        "cuenta_debito": _con_digito_verificador(
            row.get("cuenta_debito"), row.get("cuenta_debito_dv")
        ),
        "cuenta_acreditacion": _con_digito_verificador(
            row.get("cuenta_acreditacion"), row.get("cuenta_acreditacion_dv")
        ),
        "zona": _texto(row.get("zona")),
        "centro": _texto(row.get("centro")),
        "sector": _texto(row.get("sector")),
        "cuil": formatear_cuil(cuil) if len(cuil) == 11 else cuil,
        "motivo": formatear_motivo_fecha_baja(
            row.get("motivo"), row.get("fecha_baja"), motivos_config
        ),
    }
