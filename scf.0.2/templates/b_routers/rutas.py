# routers/rutas.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
# ----------------------------------------------------
from scripts.models.rutas import Rutas
# ----------------------------------------------------
from scripts.querys.rutas import get_rutas, add_rutas, put_rutas, get_rutas_by_id, search_rutas_in_db
# ----------------------------------------------------
# Importa desde el módulo externo
from utils.websockets_manager import notify_clients
rutas = APIRouter()
@rutas.get("/rutas/", response_model=List[Rutas])
async def fetch_rutas():
    try:
        return await get_rutas()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los datos: {e}"
        )
@rutas.get("/rutas/{id}/", response_model=Rutas)
async def fetch_m_entrada_by_id(id: str):
    try:
        documento= await get_rutas_by_id(id)
        if not documento:
            raise HTTPException(
                status_code=404, detail="Documento no encontrado")
        return documento
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al obtener el documento: {e}"
        )
@rutas.post("/rutas/search/", response_model=List[Rutas])
async def search_rutas(filter: Dict[str, Any]):
    try:
        documentos= await search_rutas_in_db(filter)
        print('Documentos:', documentos)
        return documentos
    except Exception as e:
        raise HTTPException(
        status_code =500, detail=f"Error al realizar la búsqueda: {e}")
@rutas.post("/rutas/", status_code=201)
async def post_rutas(rutas: Rutas):
    try:
        result = await add_rutas(rutas.dict())
        await notify_clients("rutas", "Nuevo rutas agregado")
        return {"message": "Documento insertado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al insertar el documento: {e}"
        )
@rutas.put("/rutas/")
async def update_rutas(item: Rutas):
    try:
        result= await put_rutas(item.dict())
        await notify_clients("rutas", "rutas actualizado")
        return {"message": "Documento actualizado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al actualizar el documento: {e}"
        )
