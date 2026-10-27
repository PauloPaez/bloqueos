# routers/escuelas.py
from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import StreamingResponse
from scripts.exceptions import EscuelaNotFoundError, EscuelaValidationError
from scripts.models.escuelas import (
    Escuelas,
    EscuelasResponse,
    EscuelasSearchResponse,
)
from scripts.querys.escuelas import (
    add_escuelas,
    # desbloquear_escuelas_por_dni,
    get_escuelas,
    get_escuelas_by_id,
    get_escuelas_distinct,
    patch_escuelas,
    put_escuelas,
    search_escuelas_in_db,
    search_escuelas_paginado,
)
from scripts.querys.motivos import get_motivos
from scripts.schemas.escuelas import EscuelasPatch
from scripts.schemas.schemaHabilitaciones import CerrarPeriodoRequest
from scripts.querys.habilitaciones import consultar_cierre_periodo, cerrar_habilitacion_periodo
from utils.formateoDatos import agrupar_por_concepto
from utils.generacionExcel import generar_excel_bajas
from utils.generacionZip import crear_zip

# Importa desde el módulo externo
from utils.websockets_manager import notify_clients

escuelas = APIRouter()


@escuelas.get("/escuelas/cierre-periodo/{periodo}/")
async def consultar_cierre_escuelas(periodo: str):
    try:
        return await consultar_cierre_periodo(periodo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"ERROR al consultar el cierre del período: {e}")
        raise HTTPException(status_code=500, detail="No se pudo consultar el estado de cierre del período.")


@escuelas.post("/escuelas/cerrar-periodo/")
async def cerrar_periodo_escuelas(documento: CerrarPeriodoRequest):
    try:
        resultado = await cerrar_habilitacion_periodo(documento.periodo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        print(f"ERROR al cerrar el período: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"ERROR al cerrar el período: {e}")
        raise HTTPException(status_code=500, detail="No se pudo cerrar el período.")
    for modulo in ("habilitaciones", "escuelas"):
        try:
            await notify_clients(modulo, resultado["mensaje"])
        except Exception as e:
            print(f"ERROR al notificar el cierre de {modulo}: {e}")
    return resultado


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
    except EscuelaValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
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
    except EscuelaValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EscuelaNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar el documento: {e}"
        )


@escuelas.patch("/escuelas/") #TODO: manejar mejor los errores como, que es necesario un motivo para bloquear. Habria que fortalecerlo desde el front y backend. Ya esta desde el back, solo falta retornar mejor ese mensaje
async def partial_update_escuelas(document: EscuelasPatch):
    try:
        result = await patch_escuelas(document)
        await notify_clients("escuelas", "Documento actualizado parcialmente")
        return { #cuando hubo modificaciones, mantiene en el result(diccionario), la cantidad de dnis modificados, en caso de bloqueo masivo
            "message": result["message"],
            "status": "success",
            "result": result,
        }
    except EscuelaValidationError as e:
        print(f"ERROR de validación al actualizar la escuela: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EscuelaNotFoundError as e:
        print(f"ERROR al buscar la escuela: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HTTPException as e:
        print(f"ERROR: {e.detail}")
        raise
    except Exception as e:
        print(f"ERROR al actualizar parcialmente la escuela: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar parcialmente la escuela.",
        )


# @escuelas.post("/escuelas/desbloquear-dni/")
# async def unlock_escuelas_by_dni(document: DesbloquearEscuelasPorDni):
#     try:
#         result = await desbloquear_escuelas_por_dni(document.id)
#         await notify_clients("escuelas", "Padrones del DNI desbloqueados")
#         return {"message": result["message"], "result": result}
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error al desbloquear los padrones del DNI: {e}",
#         )


@escuelas.get("/escuelas/distinct/{campo}/")
async def get_TN_distinct(campo: str):
    try:
        documento = await get_escuelas_distinct(campo)
        # if not documento:
        #     raise HTTPException(status_code=404, detail="Documento no encontrado")
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
                status_code=404, detail="No se encontraron datos para la generacion de documentos."
            )

        motivos_config = {
            item["motivo"].strip().casefold(): item.get("lleva_fecha", False)
            for item in await get_motivos()
            if item.get("motivo")
        }

        grupos = agrupar_por_concepto(resultado)
        archivos = []
        for concepto, escuelas_tipo in grupos.items():
            if not escuelas_tipo:
                continue

            contenido, _ = generar_excel_bajas(
                escuelas_tipo,
                periodo=periodo,
                fecha_pago=fecha_pago,
                motivos_config=motivos_config,
            )
            archivos.append(
                (f"bloqueo_acreditaciones_{concepto}.xlsx", contenido)
            )

        zip_generado = crear_zip(archivos)

        return StreamingResponse(
            zip_generado,
            media_type="application/zip",
            headers={
                "Content-Disposition": 'attachment; filename="bajas_acreditaciones_excel.zip"'
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
