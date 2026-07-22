# routers/usuarios.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
# ----------------------------------------------------
from scripts.models.usuarios import Usuarios
# ----------------------------------------------------
from scripts.querys.usuarios import get_usuarios, add_usuarios, put_usuarios, get_usuarios_by_id, search_usuarios_in_db, \
    patch_usuarios
# ----------------------------------------------------
# Importa desde el módulo externo
from utils.websockets_manager import notify_clients
usuarios = APIRouter()
@usuarios.get("/usuarios/", response_model=List[Usuarios])
async def fetch_usuarios():
    try:
        return await get_usuarios()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los datos: {e}"
        )
@usuarios.get("/usuarios/{id}/", response_model=Usuarios)
async def fetch_m_entrada_by_id(id: str):
    try:
        documento= await get_usuarios_by_id(id)
        if not documento:
            raise HTTPException(
                status_code=404, detail="Documento no encontrado")
        return documento
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al obtener el documento: {e}"
        )
@usuarios.post("/usuarios/search/", response_model=List[Usuarios])
async def search_usuarios(filter: Dict[str, Any]):
    try:
        documentos= await search_usuarios_in_db(filter)
        print('Documentos:', documentos)
        return documentos
    except Exception as e:
        raise HTTPException(
        status_code =500, detail=f"Error al realizar la búsqueda: {e}")
@usuarios.post("/usuarios/", status_code=201)
async def post_usuarios(usuarios: Usuarios):
    try:
        result = await add_usuarios(usuarios.dict())
        await notify_clients("usuarios", "Nuevo usuarios agregado")
        return {"message": "Documento insertado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al insertar el documento: {e}"
        )
@usuarios.put("/usuarios/")
async def update_usuarios(item: Usuarios):
    try:
        result= await put_usuarios(item.dict())
        await notify_clients("usuarios", "usuarios actualizado")
        return {"message": "Documento actualizado con éxito", "id": str(result)}
    except Exception as e:
        raise HTTPException(
            status_code =500, detail=f"Error al actualizar el documento: {e}"
        )
@usuarios.patch("/usuarios/")
async def partial_update_usuarios(document: dict):
    try:
        result = await patch_usuarios(document)
        await notify_clients("empleados", "Documento actualizado parcialmente")
        return {
            "message": "Actualización parcial exitosa",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar parcialmente el documento: {e}"
        )