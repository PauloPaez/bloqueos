"""Generación simple del Excel de bajas de acreditaciones."""

from __future__ import annotations

import io
import re
from collections.abc import Iterable, Mapping
from typing import Any

import polars as pl
import xlsxwriter
from fastapi.responses import StreamingResponse
from utils.formateoDatos import preparar_fila_baja

# TODO: Por el momento las columnas que tienen filas vacias, es porque no se como determinar los datos que llevan. Preguntar temas de diseño, ya que la primera fila, la de los nombres de las columnas, usa un renglon y en el original usa 2

EXCEL_HEADERS = (
    "Concepto",
    "Disco",
    "Nro de Padron",
    "Apellido y Nombre",
    "Importe",
    "Nro. de Cuenta",
    "Zona",
    "Centro",
    "Sector",
    "CUIL",
    "Cuenta a Debitar",
    "Motivo de baja",
    "Estructura",
    "B01",
)

# Las columnas que todavía no tienen una fuente definida se dejan vacías.
_EXCEL_FIELDS = (
    "concepto",
    None,
    "padron",
    "beneficiario_nombre",
    "importe",
    "cuenta_acreditacion",
    "zona",
    "centro",
    "sector",
    "cuil",
    "cuenta_debito",
    "motivo",
    None,
    None,
)

_MIN_COLUMN_WIDTH = 10
_MAX_COLUMN_WIDTH = 40
_COLUMN_WIDTH_PADDING = 2


def _rows(data: pl.DataFrame | Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(data, pl.DataFrame):
        return data.to_dicts()
    return [dict(row) for row in data]


def _excel_values(row: Mapping[str, Any]) -> tuple[str, ...]:
    prepared = preparar_fila_baja(row)
    return tuple(
        "" if field is None or prepared.get(field) is None else str(prepared.get(field))
        for field in _EXCEL_FIELDS
    )


def _column_widths(rows: list[tuple[str, ...]]) -> tuple[int, ...]:
    """Calcula anchos legibles a partir de encabezados y datos reales."""
    widths = []
    for column, header in enumerate(EXCEL_HEADERS):
        values = [header, *(row[column] for row in rows)]
        content_width = max(len(value) for value in values)
        width = content_width + _COLUMN_WIDTH_PADDING
        widths.append(min(max(width, _MIN_COLUMN_WIDTH), _MAX_COLUMN_WIDTH))
    return tuple(widths)


def generar_excel_bajas(
    df: pl.DataFrame | Iterable[Mapping[str, Any]],
    periodo: str | None = None,
    fecha_pago: Any = None,
) -> tuple[io.BytesIO, str]:
    """Genera un Excel plano con las columnas definidas en ``EXCEL_HEADERS``."""
    del fecha_pago  # Se conserva en la firma por compatibilidad con el endpoint.

    rows = _rows(df)
    values = [_excel_values(row) for row in rows]
    buffer = io.BytesIO()

    with xlsxwriter.Workbook(buffer, {"in_memory": True}) as workbook:
        sheet = workbook.add_worksheet("Bajas")
        header_format = workbook.add_format({"bold": True, "text_wrap": True})
        # En el futuro Importe podría usar un formato monetario; por ahora es texto.
        text_format = workbook.add_format({"num_format": "@"})

        for column, width in enumerate(_column_widths(values)):
            sheet.set_column(column, column, width)

        for column, header in enumerate(EXCEL_HEADERS):
            sheet.write_string(0, column, header, header_format)

        for row_number, row in enumerate(values, start=1):
            for column, value in enumerate(row):
                sheet.write_string(row_number, column, value, text_format)

        sheet.autofilter(0, 0, len(rows), len(EXCEL_HEADERS) - 1)
        sheet.freeze_panes(1, 0)
        sheet.hide_gridlines(0)
        sheet.set_paper(5)
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)

    buffer.seek(0)
    filename_period = re.sub(r"[^A-Za-z0-9_-]+", "_", periodo or "") or "periodo"
    return buffer, f"bajas_acreditaciones_{filename_period}.xlsx"


async def generarExcel(
    datos: Iterable[Mapping[str, Any]],
    periodo: str | None = None,
    fecha_pago: Any = None,
) -> StreamingResponse:
    """Compatibilidad con el endpoint existente, devolviendo ``StreamingResponse``."""
    buffer, filename = generar_excel_bajas(datos, periodo, fecha_pago)
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
