# routers/login.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from scripts.querys.login import get_login

# Importa desde el módulo externo
from utils.websockets_manager import notify_clients

login = APIRouter()


class UserLogin(BaseModel):
    login: str  # Si llega algo que no es texto (ej: {"$ne": ""}), FastAPI responde 422
    clave: str
    app: bool = False


@login.post("/login/")
async def search_login(datos: UserLogin):
    try:
        documentos = await get_login(datos)
        print("Documentos en Router:", documentos)
        return documentos
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al realizar la búsqueda: {e}"
        )
