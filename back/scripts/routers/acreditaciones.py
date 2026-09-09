# routers/escuelas.py
from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import StreamingResponse
from scripts.models.acreditaciones import (
    Escuelas,
    EscuelasResponse,
    EscuelasSearchResponse,
)
from scripts.querys.acreditaciones import (
    add_escuelas,
    get_escuelas,
    get_escuelas_by_id,
    get_escuelas_distinct,
    patch_escuelas,
    put_escuelas,
    search_escuelas_in_db,
    search_escuelas_paginado,
)
from scripts.querys.motivos import get_motivos
from scripts.schemas.acreditaciones import EscuelasPatch
from utils.clasificacionBancos import agrupar_por_tipo_banco
from utils.generacionExcel import generar_excel_bajas
from utils.generacionZip import crear_zip

# Importa desde el módulo externo
from utils.websockets_manager import notify_clients

acreditaciones = APIRouter()


@acreditaciones.get("/escuelas/", response_model=List[EscuelasResponse])
async def fetch_acreditaciones():
    try:
        return await get_escuelas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los datos: {e}")


@acreditaciones.get("/escuelas/{id}/", response_model=EscuelasResponse)
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


# @acreditaciones.post("/escuelas/search/", response_model=List[Escuelas])
# async def search_escuelas(filter: Dict[str, Any]):
#     try:
#         documentos = await search_escuelas_in_db(filter)
#         return documentos
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Error al realizar la búsqueda: {e}"
#         )


@acreditaciones.post("/escuelas/search/", response_model=EscuelasSearchResponse)
async def search_acreditaciones(
    filter: Dict[str, Any] = Body(default={}), page: int = 1, page_size: int = 10
):
    try:
        documentos = await search_escuelas_paginado(filter, page, page_size)
        return documentos
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al realizar la búsqueda: {e}"
        )


@acreditaciones.post("/escuelas/", status_code=201)
async def post_acreditaciones(escuelas: Escuelas):
    try:
        result = await add_escuelas(escuelas.dict())
        await notify_clients("escuelas", "Nuevo escuelas agregado")
        return {"message": "Documento insertado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al insertar el documento: {e}"
        )


@acreditaciones.put("/escuelas/")
async def update_acreditaciones(item: Escuelas):
    try:
        result = await put_escuelas(item.dict())
        await notify_clients("escuelas", "escuelas actualizado")
        return {"message": "Documento actualizado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar el documento: {e}"
        )


#TODO: Hay un problema grande por el mal uso de schemas que hay en este proyecto. Cuando envio un body con 2 campos a actualizar, id y tipo_reg, todos los demas campos del documento a actualizar, se actualizan a nulo. Tendria que fortalecer el backend arreglando esto usando schemas Pydantic
@acreditaciones.patch("/escuelas/")
async def partial_update_acreditaciones(document: EscuelasPatch):
    try:
        result = await patch_escuelas(document)
        await notify_clients("escuelas", "Documento actualizado parcialmente")
        return {"message": "Actualización parcial exitosa", "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar parcialmente el documento: {e}",
        )


@acreditaciones.get("/escuelas/distinct/{campo}/")
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


@acreditaciones.post("/escuelas/generar-excel-bloqueados")
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

        motivos_config = {
            item["motivo"].strip().casefold(): item.get("lleva_fecha", False)
            for item in await get_motivos()
            if item.get("motivo")
        }

        grupos = agrupar_por_tipo_banco(resultado)
        archivos = []
        for tipo_banco, escuelas_tipo in grupos.items():
            contenido, _ = generar_excel_bajas(
                escuelas_tipo,
                periodo=periodo,
                fecha_pago=fecha_pago,
                motivos_config=motivos_config,
            )
            archivos.append(
                (f"bajas_escuelas_{tipo_banco}.xlsx", contenido)
            )

        zip_generado = crear_zip(archivos)

        return StreamingResponse(
            zip_generado,
            media_type="application/zip",
            headers={
                "Content-Disposition": 'attachment; filename="bajas_escuelas_excel.zip"'
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al generar el excel de escuelas",
        )
