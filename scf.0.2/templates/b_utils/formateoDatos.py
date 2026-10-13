from collections.abc import Mapping
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


def _texto(valor: Any) -> str:
    return "" if valor is None else str(valor)


def _con_digito_verificador(valor: Any, digito: Any) -> str:
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


def preparar_fila_baja(escuela: Any) -> dict[str, str]:
    """Construye los valores visibles de una fila de Excel/Word.

    Esta es la única definición de formato para las columnas compartidas por
    ambos documentos. El template recibe únicamente strings ya preparados.
    """
    row = _valores_de_fila(escuela)
    cuil = _texto(row.get("cuil")).strip()

    return {
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
        "motivo": _texto(row.get("motivo")),
    }
