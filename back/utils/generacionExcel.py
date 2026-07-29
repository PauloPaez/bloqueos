import io

import polars as pl
from fastapi.responses import StreamingResponse


async def generarExcel(datos: dict) -> StreamingResponse:
    # 2. Cargar la data en un DataFrame de Polars
    df = pl.DataFrame(datos)

    # 3. Crear un buffer en memoria para guardar el Excel
    buffer = io.BytesIO()
    df.write_excel(buffer)
    buffer.seek(0)  # Regresar el puntero al inicio del archivo

    # 4. Retornar el archivo virtual como StreamingResponse
    # Set los headers para que el navegador lo entienda como una descarga
    headers = {"Content-Disposition": 'attachment; filename="escuelas_bloqueadas.xlsx"'}

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )
