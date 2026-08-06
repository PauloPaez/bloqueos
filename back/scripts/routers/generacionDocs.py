from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from scripts.querys.escuelas import search_escuelas_in_db
from utils.crearDocx import crearDocumento

routerDocs = APIRouter(prefix="/generardoc", tags=["Generacion de documentos"])


# TODO: Falta ver que es Concepto, Disco, Fecha de Pago en el word
@routerDocs.post("/")
async def generarDocumento():
    resultado = await search_escuelas_in_db({"bloqueo": True})

    if not resultado:
        raise HTTPException(
            status_code=404, detail="No se encontraron datos para el período."
        )

    doc = crearDocumento(resultado)
    return StreamingResponse(
        doc,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": 'attachment; filename="bajasescuelas.docx"'},
    )
