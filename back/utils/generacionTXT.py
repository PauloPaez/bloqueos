from utils.formateoDatos import preparar_fila_baja

#Los campos se obtienen de preparar_fila_baja
CAMPOS_TXT_BLOQUEADOS = ("padron",) #agregar aca los campos nuevos que puedan aparecer
SEPARADOR_CAMPOS_TXT = "\t"


def generar_contenido_txt(escuelas, campos=CAMPOS_TXT_BLOQUEADOS) -> bytes:
    """Genera filas de texto a partir de los campos visibles de cada escuela."""
    filas = []
    for escuela in escuelas:
        fila = preparar_fila_baja(escuela)
        valores = (str(fila.get(campo, "")) for campo in campos) #guarda un generador, (campo for campo in campos), si lleva esos parentesis con un for dentro, es un generador
        filas.append(SEPARADOR_CAMPOS_TXT.join(valores)) #aca consume el generador valores uno por uno

    return "\n".join(filas).encode("utf-8")
