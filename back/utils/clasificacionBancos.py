from collections.abc import Iterable, Mapping
from typing import Any


# La clasificación se puede ampliar o modificar desde este único lugar.
TIPOS_BANCO = {
    ("TI", False): "TIAC",
    ("SU", False): "SUAC",
    ("TI", True): "TIOtros",
    ("SU", True): "SUOtros",
}


def _valores_de_fila(acreditacion: Any) -> Mapping[str, Any]:
    if isinstance(acreditacion, Mapping):
        return acreditacion
    if hasattr(acreditacion, "model_dump"):
        return acreditacion.model_dump()
    return vars(acreditacion)


def determinar_tipo_banco(acreditacion: Any) -> str:
    fila = _valores_de_fila(acreditacion)
    tipo_archivo = str(fila.get("tipo_archivo") or "").strip().upper()
    codigo_banco = str(fila.get("cod_banco") or "").strip().zfill(2)

    familia = next(
        (prefijo for prefijo in ("TI", "SU") if tipo_archivo.startswith(prefijo)),
        None,
    )
    if familia is None:
        raise ValueError(
            f"Tipo de archivo no clasificable: {fila.get('tipo_archivo')!r}"
        )

    es_otros = "OTROS" in tipo_archivo or codigo_banco != "01"
    return TIPOS_BANCO[(familia, es_otros)]


def agrupar_por_tipo_banco(
    acreditaciones: Iterable[Any],
) -> dict[str, list[Any]]:
    grupos = {tipo: [] for tipo in TIPOS_BANCO.values()}

    for acreditacion in acreditaciones:
        grupos[determinar_tipo_banco(acreditacion)].append(acreditacion)

    return grupos
