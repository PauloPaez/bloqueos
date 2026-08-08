# routers/roles.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
# ----------------------------------------------------
from scripts.models.roles import Roles
# ----------------------------------------------------
from scripts.querys.roles import get_roles, add_roles, put_roles, get_roles_by_id, search_roles_in_db
# ----------------------------------------------------
# Importa desde el módulo externo
from utils.websockets_manager import notify_clients
roles = APIRouter()
@roles.get("/roles/", response_model=List[Roles])
async def fetch_roles():
    try:
        return await get_roles()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los datos: {e}"
        )
@roles.get("/roles/{id}/", response_model=Roles)
async def fetch_m_entrada_by_id(id: str):
    try:
        documento= await get_roles_by_id(id)
        if not documento:
            raise HTTPException(
                status_code=404, detail="Documento no encontrado")
        return documento
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al obtener el documento: {e}"
        )
@roles.post("/roles/search/", response_model=List[Roles])
async def search_roles(filter: Dict[str, Any]):
    try:
        documentos= await search_roles_in_db(filter)
        print('Documentos:', documentos)
        return documentos
    except Exception as e:
        raise HTTPException(
        status_code =500, detail=f"Error al realizar la búsqueda: {e}")
@roles.post("/roles/", status_code=201)
async def post_roles(roles: Roles):
    try:
        result = await add_roles(roles.dict())
        await notify_clients("roles", "Nuevo roles agregado")
        return {"message": "Documento insertado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al insertar el documento: {e}"
        )
@roles.put("/roles/")
async def update_roles(item: Roles):
    try:
        result= await put_roles(item.dict())
        await notify_clients("roles", "roles actualizado")
        return {"message": "Documento actualizado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al actualizar el documento: {e}"
        )
