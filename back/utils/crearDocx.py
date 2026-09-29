import io
from collections.abc import Mapping
from decimal import Decimal
from pathlib import Path

from docxtpl import DocxTemplate
from scripts.models.escuelas import Escuelas
from utils.formateoDatos import formatear_importe, preparar_fila_baja


def calcular_importe_total(escuelas:dict):
    importe_total = sum(
            (
                Decimal(str(escuela.get("importe_acreditado") or "0"))
                for escuela in escuelas
            ),
            Decimal("0"),
        )

    return importe_total

def crearDocumento(
    escuelas: list[Escuelas], motivos_config: Mapping[str, bool] | None = None
):
    # Calcula la ruta absoluta hacia back/utils desde este archivo
    # BASE_DIR = Path(__file__).resolve().parents[1] / "utils" Esta linea seria sin usar parent, que es practicamente lo mismo que parents[1]
    BASE_DIR = Path(__file__).resolve().parent  # back/utils

    # Construye la ruta absoluta hacia el archivo de la plantilla
    template_path = BASE_DIR / "templates" / "templateDocsV2.docx"

    # hay que convertir a str el path
    doc = DocxTemplate(
        str(template_path)
    )  # En el word si pongo {% tr}, espacio entre % y tr da error, tiene que ir juntos

    importe_total = calcular_importe_total(escuelas)

    filas = [preparar_fila_baja(escuela, motivos_config) for escuela in escuelas]
    concepto = filas[0]["concepto"] if filas else ""
    context = {
        "lista": filas,
        "concepto": concepto,
        "importe_total": formatear_importe(importe_total),
    }

    doc.render(context)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer
