"""Generación de la planilla ministerial de bajas de acreditaciones.

El diseño se mantiene separado de la consulta a la base de datos: este módulo
recibe un DataFrame (o datos compatibles con Polars) y devuelve el archivo en
memoria listo para ser enviado por FastAPI.
"""

# ESTE ARCHIVO QUEDO VIEJO, SU IDEA PRINCIPAL LA CAMBIE POR generacionDocs.py CON UN ENFOQUE MUCHO MAS SIMPLE
from __future__ import annotations

import io
import re
from collections.abc import Iterable, Mapping
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

import polars as pl
import xlsxwriter
from fastapi.responses import StreamingResponse
from utils.formateoDatos import preparar_fila_baja

HEADERS = (
    "Nro. de\nPadrón",
    "Apellido y Nombre",
    "Importe",
    "Cuenta a\nDebitar",
    "Nro. de\nCuenta",
    "Zona",
    "Centro",
    "Sector",
    "CUIL",
    "Motivo de Baja",
)

COLUMN_WIDTHS = (12, 27, 14, 17, 15, 8, 9, 9, 18, 35)


def _text(value: Any) -> str:
    """Convierte valores nulos a texto vacío sin mostrar ``None``."""
    return "" if value is None else str(value)


def _format_date(value: Any) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")

    raw = str(value).strip()
    for pattern in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y"):
        try:
            return datetime.strptime(raw, pattern).strftime("%d/%m/%Y")
        except ValueError:
            pass
    return raw


def _rows_and_columns(
    data: pl.DataFrame | Iterable[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    if isinstance(data, pl.DataFrame):
        return data.to_dicts(), data.columns
    rows = [dict(row) for row in data]
    columns = list(rows[0].keys()) if rows else []
    return rows, columns


# TODO: Funciona el periodo y fecha pago ingresando fechas, pero falta planificar mejor esta funcion y entender que datos se necesitan aca
def _resolve_period_and_payment(
    rows: list[dict[str, Any]], periodo: str | None, fecha_pago: Any
) -> tuple[str, str]:
    period = _text(periodo).strip()
    if not period and rows:
        period = _text(rows[0].get("periodo")).strip()

    payment = _format_date(fecha_pago)
    if not payment and rows:
        row = rows[0]
        year, month, day = (
            row.get("pago_anio"),
            row.get("pago_mes"),
            row.get("pago_dia"),
        )
        if year and month and day:
            try:
                payment = date(int(year), int(month), int(day)).strftime("%d/%m/%Y")
            except (TypeError, ValueError):
                payment = ""
    return period, payment


def generar_excel_bajas(
    df: pl.DataFrame | Iterable[Mapping[str, Any]],
    periodo: str | None = None,
    fecha_pago: Any = None,
) -> tuple[io.BytesIO, str]:
    """Genera la planilla ministerial y devuelve ``(buffer, nombre_archivo)``."""
    rows, _ = _rows_and_columns(df)
    period, payment = _resolve_period_and_payment(rows, periodo, fecha_pago)
    concept = f"SUELDO.{period}.S.O.B" if period else "SUELDO.S.O.B"

    buffer = io.BytesIO()
    with xlsxwriter.Workbook(buffer, {"in_memory": True}) as workbook:
        sheet = workbook.add_worksheet("Bajas")
        sheet.hide_gridlines(2)
        sheet.set_landscape()
        sheet.set_paper(9)  # A4
        sheet.fit_to_pages(1, 0)
        sheet.set_margins(left=0.25, right=0.25, top=0.35, bottom=0.35)
        sheet.center_horizontally()
        sheet.print_area(0, 0, 10 + len(rows), 9)
        sheet.freeze_panes(10, 0)
        sheet.repeat_rows(9, 9)

        base = {"font_name": "Arial", "font_size": 10, "valign": "vcenter"}
        title = workbook.add_format(
            {
                **base,
                "font_name": "Times New Roman",
                "font_size": 20,
                "bold": True,
                "align": "center",
            }
        )
        subtitle = workbook.add_format(
            {
                **base,
                "font_name": "Times New Roman",
                "font_size": 16,
                "bold": True,
                "align": "center",
            }
        )
        main_title = workbook.add_format(
            {
                **base,
                "font_name": "Times New Roman",
                "font_size": 14,
                "bold": True,
                "align": "center",
            }
        )
        info_label = workbook.add_format(
            {
                **base,
                "font_name": "Times New Roman",
                "bold": True,
                "align": "center",
                "border": 1,
                "text_wrap": True,
            }
        )
        info_value = workbook.add_format(
            {
                **base,
                "font_name": "Times New Roman",
                "align": "center",
                "border": 1,
                "text_wrap": True,
            }
        )
        header = workbook.add_format(
            {
                **base,
                "font_name": "Times New Roman",
                "bold": True,
                "align": "center",
                "border": 1,
                "text_wrap": True,
                "bg_color": "#E7E7E7",
            }
        )
        text_cell = workbook.add_format(
            {**base, "font_name": "Times New Roman", "align": "left", "border": 1}
        )
        # TODO: ver por que al hacer el excel, no se ve a la derecha
        centered_cell = workbook.add_format({**base, "align": "center", "border": 1})
        amount_cell = workbook.add_format({**base, "align": "right", "border": 1})

        for col, width in enumerate(COLUMN_WIDTHS):
            sheet.set_column(col, col, width)

        sheet.merge_range("A1:J1", "MINISTERIO DE EDUCACION", title)
        sheet.merge_range("A2:J2", "Secretaría Administrativa", subtitle)
        sheet.merge_range("A3:J3", "Financiera", subtitle)
        sheet.merge_range("A5:J5", "BAJA DE ACREDITACIONES BANCARIAS", main_title)
        sheet.set_row(0, 24)
        sheet.set_row(1, 18)
        sheet.set_row(2, 18)
        sheet.set_row(4, 24)
        sheet.set_row(6, 22)

        sheet.merge_range("A7:A8", "Concepto", info_label)
        sheet.merge_range("B7:C8", concept, info_value)
        sheet.merge_range("D7:D8", "Disco", info_label)
        sheet.merge_range("E7:F8", concept, info_value)
        sheet.merge_range("G7:I8", "Fecha de Pago", info_label)
        sheet.merge_range("J7:J8", payment, info_value)

        header_row = 9
        data_row = 10
        sheet.set_row(header_row, 34)
        for column, label in enumerate(HEADERS):
            sheet.write(header_row, column, label, header)

        for offset, row in enumerate(rows):
            excel_row = data_row + offset
            prepared = preparar_fila_baja(row)
            values = tuple(prepared.values())
            for column, value in enumerate(values):
                if column == 2 and value is not None:
                    # TODO: Verificar esto, quiza sea mejor agregarlo al conjunto de abajo. Ademas, falta verificar que pasa si recibe como importe 300 o 1, porque si recibe un numero <1000, lo convierte a decimal moviendo el 0 a la izquierda
                    sheet.write(excel_row, column, value, amount_cell)
                if column in (0, 5, 6, 7, 8):
                    sheet.write(excel_row, column, value, centered_cell)
                else:
                    sheet.write(excel_row, column, value, text_cell)
            sheet.set_row(excel_row, 20)

    buffer.seek(0)
    filename_period = re.sub(r"[^A-Za-z0-9_-]+", "_", period) or "periodo"
    return buffer, f"bajas_acreditaciones_{filename_period}.xlsx"


async def generarExcel(
    datos: Iterable[Mapping[str, Any]],
    periodo: str | None = None,
    fecha_pago: Any = None,
) -> StreamingResponse:
    """Compatibilidad con el endpoint existente, devolviendo StreamingResponse."""
    buffer, filename = generar_excel_bajas(pl.DataFrame(datos), periodo, fecha_pago)
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
