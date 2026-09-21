from collections.abc import Iterable, Mapping
from typing import Any


ABREVIACIONES_BANCO = {
    "TIOtros": "T.O.B",
    "SUOtros": "S.O.B",
    "TIAC": "T.B.S.J",
    "SUAC": "S.B.S.J",
}

# La clasificación se puede ampliar o modificar desde este único lugar.
TIPOS_BANCO = {
    ("TI", False): "TIAC",
    ("SU", False): "SUAC",
    ("TI", True): "TIOtros",
    ("SU", True): "SUOtros",
}


def _valores_de_fila(escuela: Any) -> Mapping[str, Any]:
    if isinstance(escuela, Mapping):
        return escuela
    if hasattr(escuela, "model_dump"):
        return escuela.model_dump()
    return vars(escuela)

def determinar_abreviacion_tipo_banco(escuela: Any) -> str:
    tipo_banco = determinar_tipo_banco(escuela)
    return ABREVIACIONES_BANCO[tipo_banco]

def determinar_tipo_banco(escuela: Any) -> str:
    fila = _valores_de_fila(escuela)
    tipo_archivo = str(fila.get("tipo_archivo") or "").strip().upper()
    codigo_banco = str(fila.get("cod_banco") or "").strip().zfill(2) #zfill agrega ceros hasta tener dos caracteres 1 a 01

    if tipo_archivo.startswith("TI"):
        familia= "TI"
    elif tipo_archivo.startswith("SU"):
        familia="SU"
    else:
        familia=None

    if familia is None:
        raise ValueError(
            f"Tipo de archivo no clasificable: {fila.get('tipo_archivo')!r}"
        )

    es_otros = "OTROS" in tipo_archivo or codigo_banco != "01"
    return TIPOS_BANCO[(familia, es_otros)]


def agrupar_por_tipo_banco(escuelas: Iterable[Any]) -> dict[str, list[Any]]:
    grupos = {tipo: [] for tipo in TIPOS_BANCO.values()}

    for escuela in escuelas:
        grupos[determinar_tipo_banco(escuela)].append(escuela)

    return grupos
