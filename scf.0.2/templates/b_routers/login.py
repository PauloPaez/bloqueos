# routers/login.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
# ----------------------------------------------------
from scripts.querys.login import get_login
# ----------------------------------------------------
# Importa desde el módulo externo
from utils.websockets_manager import notify_clients
login = APIRouter()

@login.post("/login/")
async def search_login(filter: Dict[str, Any]):
    try:
        documentos= await get_login(filter)
        print('Documentos en Router:', documentos)
        return documentos
    except Exception as e:
        raise HTTPException(
        status_code =500, detail=f"Error al realizar la búsqueda: {e}")