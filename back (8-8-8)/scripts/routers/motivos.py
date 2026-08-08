# routers/motivos.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
# ----------------------------------------------------
from scripts.models.motivos import Motivos
# ----------------------------------------------------
from scripts.querys.motivos import get_motivos, add_motivos, \
    put_motivos, get_motivos_by_id, search_motivos_in_db,\
    patch_motivos, get_motivos_distinct
# ----------------------------------------------------
# Importa desde el módulo externo
from utils.websockets_manager import notify_clients
motivos = APIRouter()
@motivos.get("/motivos/", response_model=List[Motivos])
async def fetch_motivos():
    try:
        return await get_motivos()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los datos: {e}"
        )
@motivos.get("/motivos/{id}/", response_model=Motivos)
async def fetch_m_entrada_by_id(id: str):
    try:
        documento= await get_motivos_by_id(id)
        if not documento:
            raise HTTPException(
                status_code=404, detail="Documento no encontrado")
        return documento
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al obtener el documento: {e}"
        )
@motivos.post("/motivos/search/", response_model=List[Motivos])
async def search_motivos(filter: Dict[str, Any]):
    try:
        documentos= await search_motivos_in_db(filter)
        return documentos
    except Exception as e:
        raise HTTPException(
        status_code =500, detail=f"Error al realizar la búsqueda: {e}"
        )
@motivos.post("/motivos/", status_code=201)
async def post_motivos(motivos: Motivos):
    try:
        result = await add_motivos(motivos.dict())
        await notify_clients("motivos", "Nuevo motivos agregado")
        return {"message": "Documento insertado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
        status_code =500, detail=f"Error al insertar el documento: {e}"
    )
@motivos.put("/motivos/")
async def update_motivos(item: Motivos):
    try:
        result= await put_motivos(item.dict())
        await notify_clients("motivos", "motivos actualizado")
        return {"message": "Documento actualizado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al actualizar el documento: {e}"
        )
@motivos.patch("/motivos/")
async def partial_update_motivos(document: dict):
    try:
        result = await patch_motivos(document)
        await notify_clients("motivos", "Documento actualizado parcialmente")
        return {
            "message": "Actualización parcial exitosa",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar parcialmente el documento: {e}"
        )
@motivos.get("/motivos/distinct/{campo}/")
async def get_TN_distinct(campo: str):
    try:
        documento= await get_motivos_distinct(campo)
        if not documento:
            raise HTTPException(
                status_code=404, detail="Documento no encontrado")
        return documento
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al obtener el documento: {e}"
        )