PREFIJOS = [ #esta en su propio archivo ya que es importado por la descarga y la generacion de padrones
    "SUAC",
    "TIAC",
]


def es_archivo_padron(nombre, periodo):
    return nombre.startswith(tuple(PREFIJOS)) and nombre.endswith(f".{periodo}")
