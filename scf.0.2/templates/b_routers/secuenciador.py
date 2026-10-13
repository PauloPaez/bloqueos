# routers/secuenciador.py
from fastapi import APIRouter, HTTPException
# ----------------------------------------------------
from scripts.querys.secuenciador import get_secuencia
# ----------------------------------------------------
secuencia = APIRouter()

@secuencia.get("/secuencia/{nombre}/")
async def obtener_secuencia(nombre: str):
    try:
        resultado = await get_secuencia(nombre)
        return {"secuencia": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la secuencia: {str(e)}")
