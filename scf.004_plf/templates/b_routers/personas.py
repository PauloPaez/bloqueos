# routers/personas.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
# ----------------------------------------------------
from scripts.models.personas import Personas
# ----------------------------------------------------
from scripts.querys.personas import get_personas, add_personas, \
    put_personas, get_personas_by_id, search_personas_in_db,\
    patch_personas, get_personas_distinct
# ----------------------------------------------------
# Importa desde el módulo externo
from utils.websockets_manager import notify_clients
personas = APIRouter()
@personas.get("/personas/", response_model=List[Personas])
async def fetch_personas():
    try:
        return await get_personas()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los datos: {e}"
        )
@personas.get("/personas/{id}/", response_model=Personas)
async def fetch_m_entrada_by_id(id: str):
    try:
        documento= await get_personas_by_id(id)
        if not documento:
            raise HTTPException(
                status_code=404, detail="Documento no encontrado")
        return documento
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al obtener el documento: {e}"
        )
@personas.post("/personas/search/", response_model=List[Personas])
async def search_personas(filter: Dict[str, Any]):
    try:
        documentos= await search_personas_in_db(filter)
        return documentos
    except Exception as e:
        raise HTTPException(
        status_code =500, detail=f"Error al realizar la búsqueda: {e}"
        )
@personas.post("/personas/", status_code=201)
async def post_personas(personas: Personas):
    try:
        result = await add_personas(personas.dict())
        await notify_clients("personas", "Nuevo personas agregado")
        return {"message": "Documento insertado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
        status_code =500, detail=f"Error al insertar el documento: {e}"
    )
@personas.put("/personas/")
async def update_personas(item: Personas):
    try:
        result= await put_personas(item.dict())
        await notify_clients("personas", "personas actualizado")
        return {"message": "Documento actualizado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al actualizar el documento: {e}"
        )
@personas.patch("/personas/")
async def partial_update_personas(document: dict):
    try:
        result = await patch_personas(document)
        await notify_clients("personas", "Documento actualizado parcialmente")
        return {
            "message": "Actualización parcial exitosa",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar parcialmente el documento: {e}"
        )
@personas.get("/personas/distinct/{campo}/")
async def get_TN_distinct(campo: str):
    try:
        documento= await get_personas_distinct(campo)
        if not documento:
            raise HTTPException(
                status_code=404, detail="Documento no encontrado")
        return documento
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al obtener el documento: {e}"
        )
