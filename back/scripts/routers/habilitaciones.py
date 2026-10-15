# routers/habilitaciones.py
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from scripts.models.habilitaciones import Habilitaciones
from scripts.querys.habilitaciones import (
    add_habilitaciones,
    get_habilitaciones,
    get_habilitaciones_by_id,
    get_habilitaciones_distinct,
    patch_habilitaciones,
    put_habilitaciones,
    search_habilitaciones_in_db,
)
from utils.websockets_manager import notify_clients

habilitaciones = APIRouter()


@habilitaciones.get("/habilitaciones/", response_model=List[Habilitaciones])
async def fetch_habilitaciones():
    try:
        return await get_habilitaciones()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los datos: {e}"
        )
@habilitaciones.get("/habilitaciones/{id}/", response_model=Habilitaciones)
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
@habilitaciones.post("/habilitaciones/search/", response_model=List[Habilitaciones])
async def search_habilitaciones(filter: Dict[str, Any]):
    try:
        documentos= await search_habilitaciones_in_db(filter)
        return documentos
    except Exception as e:
        raise HTTPException(
        status_code =500, detail=f"Error al realizar la búsqueda: {e}"
        )
@habilitaciones.post("/habilitaciones/", status_code=201)
async def post_habilitaciones(habilitaciones: Habilitaciones):
    try:
        result = await add_habilitaciones(habilitaciones.dict())
        await notify_clients("habilitaciones", "Nuevo habilitaciones agregado")
        return {"message": "Documento insertado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
        status_code =500, detail=f"Error al insertar el documento: {e}"
    )
@habilitaciones.put("/habilitaciones/")
async def update_habilitaciones(item: Habilitaciones):
    try:
        result= await put_habilitaciones(item.dict())
        await notify_clients("habilitaciones", "habilitaciones actualizado")
        return {"message": "Documento actualizado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al actualizar el documento: {e}"
        )
@habilitaciones.patch("/habilitaciones/")
async def partial_update_habilitaciones(document: dict):
    try:
        result = await patch_habilitaciones(document)
        if result["status"] == "failed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
        await notify_clients("habilitaciones", "Documento actualizado parcialmente")
        return {
            "message": "Actualización parcial exitosa",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar parcialmente el documento: {e}"
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