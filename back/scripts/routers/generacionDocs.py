from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from scripts.querys.escuelas import search_escuelas_in_db
from scripts.querys.motivos import get_motivos
from utils.clasificacionBancos import agrupar_por_tipo_banco
from utils.crearDocx import crearDocumento
from utils.generacionZip import crear_zip

routerDocs = APIRouter(prefix="/generardoc", tags=["Generacion de documentos"])


@routerDocs.post("/")
async def generarDocumento():
    resultado = await search_escuelas_in_db({"bloqueo": True, "activo": True})

    if not resultado:
        raise HTTPException(
            status_code=404, detail="No se encontraron datos para el período."
        )

    motivos_config = {
        item["motivo"].strip().casefold(): item.get("lleva_fecha", False)
        for item in await get_motivos()
        if item.get("motivo")
    }

    grupos = agrupar_por_tipo_banco(resultado)
    archivos = (
        (
            f"bajas_escuelas_{tipo_banco}.docx",
            crearDocumento(escuelas, motivos_config),
        )
        for tipo_banco, escuelas in grupos.items()
    )
    zip_generado = crear_zip(archivos)

    return StreamingResponse(
        zip_generado,
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="bajas_escuelas_docx.zip"'},
    )
