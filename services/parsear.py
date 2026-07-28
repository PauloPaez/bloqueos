from decimal import Decimal


LAYOUT = [
    ("tipo_reg",                1,   1),
    ("cod_liquidacion",         2,   3),
    ("centro_pago",             4,   6),
    ("pago_anio",               7,   8),
    ("pago_mes",                9,  10),
    ("pago_dia",               11,  12),
    ("suc_acreditacion",       13,  14),
    ("tipo_acreditacion",      15,  15),
    ("cuenta_acreditacion",    16,  22),
    ("cuenta_acreditacion_dv", 23,  23),
    ("importe_acreditado",     24,  38),
    ("beneficiario_nombre",    39,  68),
    ("documento_tipo",         69,  69),
    ("documento_nro",          70,  77),
    ("suc_debito",             78,  79),
    ("tipo_debito",            80,  80),
    ("cuenta_debito",          81,  87),
    ("cuenta_debito_dv",       88,  88),
    ("cuil",                   89,  99),
    ("zona",                  100, 100),
    ("centro",                101, 102),
    ("sector",                103, 105),
    ("padron",                106, 111),
    ("padron_dv",             112, 112),
    ("reservado",             113, 126),
    ("cod_banco",             127, 128),
]

def parsear_registro(linea: str) -> dict:
    """
    Convierte un registro COBOL de 128 caracteres en un diccionario.
    """

    linea = linea.rstrip("\r\n")

    if len(linea) != 128:
        raise ValueError(
            f"Registro inválido. Largo={len(linea)}. Debe ser 128."
        )

    registro = {}

    for campo, inicio, fin in LAYOUT:
        valor = linea[inicio - 1:fin]

        if campo == "IMPORTE_ACREDITADO":
            valor = Decimal(valor) / Decimal("100")

        elif campo in ("BENEFICIARIO_NOMBRE", "RESERVADO"):
            valor = valor.rstrip()

        else:
            valor = valor.strip()

        registro[campo] = valor

    return registro
