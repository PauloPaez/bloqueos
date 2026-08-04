import io
import os
from pathlib import Path

from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from scripts.models.escuelas import Escuelas
from scripts.querys.escuelas import search_escuelas_in_db
from utils.formateoDatos import preparar_fila_baja

routerDocs = APIRouter(prefix="/generardoc", tags=["Generacion de documentos"])


# TODO: Hay un tema, que se manda a descargar desde el front y automaticamente sale para descargar el zip. Pero que pasa si cancela la ventana por error? ya no tiene forma de volver a obtener ese examen y tendria que generar uno nuevo. Hay que ver si es mejor tener la posibilidad de volver a descargar un examen o generar uno nuevo en caso de ese error
def crearDocumento(escuelas: list[Escuelas]):
    # Calcula la ruta absoluta hacia back/utils desde este archivo
    BASE_DIR = Path(__file__).resolve().parents[2] / "utils"

    # Construye la ruta absoluta hacia el archivo de la plantilla
    template_path = BASE_DIR / "templates" / "templateDocs.docx"

    # Tienes que convertirlo a string con str(template_path)
    doc = DocxTemplate(
        str(template_path)
    )  # En el word si pongo {% tr}, espacio entre % y tr da error, tiene que ir juntos

    context = {"lista": [preparar_fila_baja(escuela) for escuela in escuelas]}

    doc.render(context)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer


# TODO: Falta ver que es Concepto, Disco, Fecha de Pago en el word
@routerDocs.get("/")
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
