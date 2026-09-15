from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from scripts.querys.acreditaciones import search_acreditaciones_in_db
from scripts.querys.motivos import get_motivos
from utils.clasificacionBancos import agrupar_por_tipo_banco
from utils.crearDocx import crearDocumento
from utils.generacionZip import crear_zip

routerDocs = APIRouter(prefix="/generardoc", tags=["Generacion de documentos"])

#Aca genero los DOCX, los excel son generados en los endpoints de acreditaciones. TODO: Podria mejorar el orden y poner el endpoint de los excel en este archivo
#TODO: Verificar si es confiable el resultado total de todas las acreditaciones bloqueadas por docx, quiza se pueda hacer mas seguro
@routerDocs.post("/")
async def generarDocumento():
    resultado = await search_acreditaciones_in_db({"bloqueo": True, "activo": True})

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
            f"bajas_acreditaciones_{tipo_banco}.docx",
            crearDocumento(acreditaciones, motivos_config),
        )
        for tipo_banco, acreditaciones in grupos.items()
    )
    zip_generado = crear_zip(archivos)

    return StreamingResponse(
        zip_generado,
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="bajas_acreditaciones_docx.zip"'},
    )
