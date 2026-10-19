# routers/habilitaciones.py
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status
from scripts.querys.habilitaciones import (
    get_habilitaciones,
    get_habilitaciones_by_id,
    get_habilitaciones_distinct,
    patch_habilitaciones,
    put_habilitaciones,
    search_habilitaciones_in_db,
)
from scripts.schemas.schemaHabilitaciones import (
    HabilitacionesCreate,
    HabilitacionesResponse,
    HabilitacionesUpdate,
    normalizar_periodo,
)
from utils.websockets_manager import notify_clients
from utils.padrones.cargarHabilitacion import crear_habilitacion_con_padron

habilitaciones = APIRouter()


@habilitaciones.get("/habilitaciones/", response_model=List[HabilitacionesResponse])
async def fetch_habilitaciones():
    try:
        return await get_habilitaciones()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los datos: {e}"
        )


@habilitaciones.get("/habilitaciones/{id}/", response_model=HabilitacionesResponse)
async def fetch_m_entrada_by_id(id: str):
    try:
        documento= await get_habilitaciones_by_id(id)
        if not documento:
            raise HTTPException(
                status_code=404, detail="Documento no encontrado")
        return documento
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al obtener el documento: {e}"
        )


@habilitaciones.post("/habilitaciones/search/", response_model=List[HabilitacionesResponse])
async def search_habilitaciones(filter: Dict[str, Any]):
    try:
        documentos= await search_habilitaciones_in_db(filter)
        return documentos
    except Exception as e:
        raise HTTPException(
        status_code =500, detail=f"Error al realizar la búsqueda: {e}"
        )


@habilitaciones.post("/habilitaciones/", status_code=201)
async def post_habilitaciones(habilitacion: HabilitacionesCreate):
    try:
        result = await crear_habilitacion_con_padron(habilitacion.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail="Error al iniciar la carga de acreditaciones")

    # Una notificación fallida no revierte ni invalida una carga que ya terminó correctamente.
    for modulo in ("escuelas", "habilitaciones"):
        try:
            await notify_clients(modulo, "Acreditaciones cargadas y habilitación registrada")
        except Exception as e:
            print(f"ERROR al notificar {modulo}: {e}")
    return {"message": "Acreditaciones cargadas y habilitación registrada", **result}


@habilitaciones.put("/habilitaciones/")
async def update_habilitaciones(item: HabilitacionesUpdate):
    try:
        result= await put_habilitaciones(item.model_dump(exclude_unset=True))
        await notify_clients("habilitaciones", "habilitaciones actualizado")
        return {"message": "Documento actualizado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al actualizar el documento: {e}"
        )


@habilitaciones.patch("/habilitaciones/")
async def partial_update_habilitaciones(habilitacion: HabilitacionesUpdate):
    try:
        result = await patch_habilitaciones(habilitacion.model_dump(exclude_unset=True))
        if result["status"] == "failed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
        await notify_clients("habilitaciones", "Documento actualizado parcialmente")
        return {
            "message": "Actualización parcial exitosa",
            "result": result
        }
    except HTTPException as e:
        print(f"ERROR: {e.detail}")
        raise
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(
            status_code=500, detail="Error al actualizar parcialmente la habilitacion"
        )


@habilitaciones.get("/habilitaciones/distinct/{campo}/")
async def get_TN_distinct(campo: str):
    try:
        documento= await get_habilitaciones_distinct(campo)
        if not documento:
            raise HTTPException(
                status_code=404, detail="Documento no encontrado")
        return documento
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al obtener el documento: {e}"
        )
