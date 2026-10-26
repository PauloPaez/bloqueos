from utils.formateoDatos import preparar_fila_baja
from utils.padrones.prefijos import PREFIJOS

#Los campos se obtienen de preparar_fila_baja
CAMPOS_TXT_BLOQUEADOS = ("padron",) #agregar aca los campos nuevos que puedan aparecer
SEPARADOR_CAMPOS_TXT = "\t"


def generar_contenido_txt(escuelas, campos=CAMPOS_TXT_BLOQUEADOS) -> bytes:
    """Genera filas de texto a partir de los campos visibles de cada escuela."""
    filas = []
    for escuela in escuelas:
        fila = preparar_fila_baja(escuela)
        valores = ( #guarda un generador, (campo for campo in campos), si lleva esos parentesis con un for dentro, es un generador
            str(fila.get(campo, "")).replace("/", "")
            if campo == "padron"
            else str(fila.get(campo, ""))
            for campo in campos
        )
        filas.append(SEPARADOR_CAMPOS_TXT.join(valores)) #aca consume el generador valores uno por uno. A partir de aca, es donde valores comienza a ejecutarse

    return "\n".join(filas).encode("utf-8")


def generar_txt_por_archivo(bloqueados, periodo):
    """Agrupa la selección del cierre y conserva el formato del TXT de padrones."""
    grupos = {}
    for registro in bloqueados:
        tipo = registro.get("tipo_archivo")
        if (not isinstance(tipo, str) or not tipo.startswith(tuple(PREFIJOS))
                or any(caracter in tipo for caracter in '/\\\x00')):
            raise ValueError("Hay bloqueados sin un archivo de origen válido.")
        if registro.get("periodo") != periodo:
            raise ValueError("Hay bloqueados que no corresponden al período de cierre.")
        grupos.setdefault(tipo, []).append(registro)
    return {
        f"BLOQUEO-{tipo}.{periodo}.txt": generar_contenido_txt(registros)
        for tipo, registros in sorted(grupos.items())
    }
