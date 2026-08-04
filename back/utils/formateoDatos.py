from decimal import Decimal


def formatear_importe(valor: str) -> float:
    print("Entro a formatear?")
    importe = Decimal(valor) / Decimal("100")
    parte_entera, parte_decimal = f"{importe:.2f}".split(".")
    parte_entera_formateada = f"{int(parte_entera):,}".replace(",", ".")
    print("Llega a return?")
    return f"{parte_entera_formateada},{parte_decimal}"


def formatear_cuil(cuil: str) -> str:
    return f"{cuil[:2]}-{cuil[2:10]}-{cuil[10]}"


if __name__ == "__main__":
    print(formatear_importe("200.5"))
