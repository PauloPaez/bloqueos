from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from scripts.querys.escuelas import search_escuelas_in_db
from scripts.querys.motivos import get_motivos
from utils.clasificacionBancos import agrupar_por_tipo_banco
from utils.crearDocx import crearDocumento
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

    grupos = agrupar_por_tipo_banco(resultado) #obtengo las escuelas bloqueadas pero divididas por grupos
    archivos = ( #(expresion for elemento in iterable if condicion) funcion generadora. Al ser un generador, la variable archivo recien toma valor cuando es iterada en la funcion crear_zip... Por cada vuelta el for de esa funcion le pide al generador el siguiente resultado. No procesa todos los grupos en la primera llamada a crear_zip, pero tampoco procesa solo uno: procesa uno, lo agrega al ZIP, pide el siguiente y sigue hasta terminar
        (
            f"bajas_acreditaciones_{tipo_banco}.docx",
            crearDocumento(escuelas, motivos_config),
        )
        for tipo_banco, escuelas in grupos.items()
        if escuelas
    )
    zip_generado = crear_zip(archivos)

    return StreamingResponse(
        zip_generado,
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="bajas_acreditaciones_docx.zip"'},
    )
