import io
from pathlib import Path

from docxtpl import DocxTemplate
from scripts.models.escuelas import Escuelas
from utils.formateoDatos import preparar_fila_baja


# TODO: Hay un tema, que se manda a descargar desde el front y automaticamente sale para descargar el zip. Pero que pasa si cancela la ventana por error? ya no tiene forma de volver a obtener ese examen y tendria que generar uno nuevo. Hay que ver si es mejor tener la posibilidad de volver a descargar un examen o generar uno nuevo en caso de ese error
def crearDocumento(escuelas: list[Escuelas]):
    # Calcula la ruta absoluta hacia back/utils desde este archivo
    # BASE_DIR = Path(__file__).resolve().parents[1] / "utils" Esta linea seria sin usar parent, que es practicamente lo mismo que parents[1]
    BASE_DIR = Path(__file__).resolve().parent  # back/utils
    print(BASE_DIR)

    # Construye la ruta absoluta hacia el archivo de la plantilla
    template_path = BASE_DIR / "templates" / "templateDocs.docx"

    # hay que convertir a str el path
    doc = DocxTemplate(
        str(template_path)
    )  # En el word si pongo {% tr}, espacio entre % y tr da error, tiene que ir juntos

    context = {"lista": [preparar_fila_baja(escuela) for escuela in escuelas]}

    doc.render(context)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer
