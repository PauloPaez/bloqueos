from utils.formateoDatos import preparar_fila_baja

#Los campos se obtienen de preparar_fila_baja
CAMPOS_TXT_BLOQUEADOS = ("padron",) #agregar aca los campos nuevos que puedan aparecer
SEPARADOR_CAMPOS_TXT = "\t"


def generar_contenido_txt(escuelas, campos=CAMPOS_TXT_BLOQUEADOS) -> bytes:
    """Genera filas de texto a partir de los campos visibles de cada escuela."""
    filas = (
        SEPARADOR_CAMPOS_TXT.join(
            str(fila.get(campo, ""))
            for campo in campos
        )
        for escuela in escuelas
        for fila in [preparar_fila_baja(escuela)]
    )
    return "\n".join(filas).encode("utf-8")
