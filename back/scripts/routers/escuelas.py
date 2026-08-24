# routers/escuelas.py
from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException
from scripts.models.escuelas import (
    Escuelas,
    EscuelasResponse,
    EscuelasSearchResponse,
)
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
from scripts.schemas.escuelas import EscuelasPatch
from utils.generacionExcel import generarExcel

# Importa desde el módulo externo
from utils.websockets_manager import notify_clients

escuelas = APIRouter()


@escuelas.get("/escuelas/", response_model=List[EscuelasResponse])
async def fetch_escuelas():
    try:
        return await get_escuelas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los datos: {e}")


@escuelas.get("/escuelas/{id}/", response_model=EscuelasResponse)
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


@escuelas.post("/escuelas/search/", response_model=EscuelasSearchResponse)
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
async def partial_update_escuelas(document: EscuelasPatch):
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


@escuelas.post("/escuelas/generar-excel-bloqueados")
async def generarExcelBloqueados(
    periodo: str | None = None, fecha_pago: str | None = None
):
    """Genera la planilla de bajas para el período y fecha indicados. Los parametros de entrada son opcionales"""
    try:
        # 1. Obtener la data (lista de diccionarios)
        resultado = await search_escuelas_in_db({"bloqueo": True, "activo": True})

        if not resultado:
            raise HTTPException(
                status_code=404, detail="No se encontraron datos para el período."
            )

        excelGenerado = await generarExcel(
            resultado, periodo=periodo, fecha_pago=fecha_pago
        )

        return excelGenerado

    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al generar el excel de escuelas",
        )
