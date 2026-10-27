from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from scripts.querys.escuelas import search_escuelas_in_db
from scripts.querys.habilitaciones import search_habilitaciones_in_db
from scripts.querys.motivos import get_motivos
from utils.crearDocx import crearDocumento
from utils.formateoDatos import agrupar_por_concepto
from utils.generacionZip import crear_zip

routerDocs = APIRouter(prefix="/generardoc", tags=["Generacion de documentos"])

#Logica para tipo de banco en cabecera: X.O.B para Otros bancos, X puede ser S de suplentes o T de titulares
#X.B.S.J es para Banco San Juan, X puede ser S de suplentes o T de titulares.

@routerDocs.post("/")
async def generarDocumento():
    """**Este endpoint genera documentos DOCX**"""
    resultado = await search_escuelas_in_db({"bloqueo": True, "activo": True})

    if not resultado:
        raise HTTPException(
            status_code=404, detail="No se encontraron datos para la generacion de documentos."
        )

    motivos_config = {
        item["motivo"].strip().casefold(): item.get("lleva_fecha", False)
        for item in await get_motivos()
        if item.get("motivo")
    }

    grupos = agrupar_por_concepto(resultado)
    archivos = []
    for concepto, escuelas in grupos.items():
        periodo = escuelas[0]["periodo"]
        habilitaciones = await search_habilitaciones_in_db(
            {"periodo": periodo, "activo": True}
        )
        if len(habilitaciones) != 1:
            raise HTTPException(
                status_code=400,
                detail=f"Debe existir una única habilitación activa para el período {periodo}.",
            )
        fecha_pago = habilitaciones[0].get("fecha_pago")
        if fecha_pago is None:
            raise HTTPException(
                status_code=400,
                detail=f"Complete la fecha de pago de la habilitación {periodo} antes de generar el DOCX.",
            )
        archivos.append(
            (
                f"bloqueo_acreditaciones_{concepto}.docx",
                crearDocumento(escuelas, motivos_config, fecha_pago=fecha_pago),
            )
        )

    zip_generado = crear_zip(archivos)

    return StreamingResponse(
        zip_generado,
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="bajas_acreditaciones_docx.zip"'},
    )
