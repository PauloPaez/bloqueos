import io

import polars as pl
import xlsxwriter
from fastapi.responses import StreamingResponse


async def generarExcel(datos: dict) -> StreamingResponse:
    # 1. Cargar la data en un DataFrame de Polars
    df = pl.DataFrame(datos)

    # 2. Crear un buffer en memoria para guardar el Excel
    buffer = io.BytesIO()

    # 3. Crear el workbook apuntando al buffer
    with xlsxwriter.Workbook(buffer, {"in_memory": True}) as wb:
        ws = wb.add_worksheet("Hoja1")

        # Formato del título
        fmt_titulo = wb.add_format(
            {
                "font_size": 18,
                "bold": True,
                "align": "center",
                "valign": "vcenter",
            }
        )

        # Fusionar celdas dinámicamente según el número de columnas del DataFrame
        last_col = xlsxwriter.utility.xl_col_to_name(df.width - 1)
        ws.merge_range(f"A1:{last_col}1", "MINISTERIO DE EDUCACION", fmt_titulo)

        # Ajustar altura de la fila del título
        ws.set_row(0, 30)

        # 4. Escribir el DataFrame a partir de la fila 3
        df.write_excel(
            workbook=wb,
            worksheet=ws,
            position="A3",
            table_style="Table Style Medium 4",
            autofit=True,
            # hide_gridlines=True,
        )

    # 5. Regresar el puntero al inicio del buffer
    buffer.seek(0)

    # 6. Retornar el archivo como StreamingResponse
    headers = {"Content-Disposition": 'attachment; filename="escuelas_bloqueadas.xlsx"'}

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )
