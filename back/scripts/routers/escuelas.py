# routers/escuelas.py
from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.responses import StreamingResponse
import polars as pl
import io
from pydantic import BaseModel

# ----------------------------------------------------
from scripts.models.escuelas import Escuelas

# ----------------------------------------------------
from scripts.querys.escuelas import (
    add_escuelas,
    get_escuelas,
    get_escuelas_by_id,
    get_escuelas_distinct,
    patch_escuelas,
    put_escuelas,
    search_escuelas_in_db,
    search_escuelas_paginado,
)

# ----------------------------------------------------
# Importa desde el módulo externo
from utils.websockets_manager import notify_clients

escuelas = APIRouter()


@escuelas.get("/escuelas/", response_model=List[Escuelas])
async def fetch_escuelas():
    try:
        return await get_escuelas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los datos: {e}")


@escuelas.get("/escuelas/{id}/", response_model=Escuelas)
async def fetch_m_entrada_by_id(id: str):
    try:
        documento = await get_escuelas_by_id(id)
        if not documento:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return documento
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el documento: {e}"
        )


# @escuelas.post("/escuelas/search/", response_model=List[Escuelas])
# async def search_escuelas(filter: Dict[str, Any]):
#     try:
#         documentos = await search_escuelas_in_db(filter)
#         return documentos
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Error al realizar la búsqueda: {e}"
#         )


@escuelas.post("/escuelas/search/")
async def search_escuelas(
    filter: Dict[str, Any] = Body(default={}), page: int = 1, page_size: int = 10
):
    try:
        documentos = await search_escuelas_paginado(filter, page, page_size)
        return documentos
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al realizar la búsqueda: {e}"
        )


@escuelas.post("/escuelas/", status_code=201)
async def post_escuelas(escuelas: Escuelas):
    try:
        result = await add_escuelas(escuelas.dict())
        await notify_clients("escuelas", "Nuevo escuelas agregado")
        return {"message": "Documento insertado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al insertar el documento: {e}"
        )


@escuelas.put("/escuelas/")
async def update_escuelas(item: Escuelas):
    try:
        result = await put_escuelas(item.dict())
        await notify_clients("escuelas", "escuelas actualizado")
        return {"message": "Documento actualizado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar el documento: {e}"
        )


@escuelas.patch("/escuelas/")
async def partial_update_escuelas(document: dict):
    try:
        result = await patch_escuelas(document)
        await notify_clients("escuelas", "Documento actualizado parcialmente")
        return {"message": "Actualización parcial exitosa", "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar parcialmente el documento: {e}",
        )


@escuelas.get("/escuelas/distinct/{campo}/")
async def get_TN_distinct(campo: str):
    try:
        documento = await get_escuelas_distinct(campo)
        if not documento:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return documento
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el documento: {e}"
        )


@escuelas.post(
    "/generar-excel-bloqueados"
)  # Este endpoint lo hice en un momento cuando pidieron trabajar con excel, pero luego dijeron que se iba a trabajar desde frontend
async def obtenerPartePoliciaImponibleExcel():
    """Este endpoint por el momento no recibe nada pero genera un excel unicamente con las escuelas bloqueadas."""
    try:
        # 1. Obtener la data (lista de diccionarios)
        resultado = await search_escuelas_in_db({"bloqueo": True})
        print(resultado)

        if not resultado:
            raise HTTPException(
                status_code=404, detail="No se encontraron datos para el período."
            )

        # 2. Cargar la data en un DataFrame de Polars
        df = pl.DataFrame(resultado)

        # 3. Crear un buffer en memoria para guardar el Excel
        buffer = io.BytesIO()
        df.write_excel(buffer)
        buffer.seek(0)  # Regresar el puntero al inicio del archivo

        # 4. Retornar el archivo virtual como StreamingResponse
        # Set los headers para que el navegador lo entienda como una descarga
        headers = {
            "Content-Disposition": 'attachment; filename="escuelas_bloqueadas.xlsx"'
        }

        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al generar el excel del PARTE_POLICIA_IMPONIBLE",
        )
