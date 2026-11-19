from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

ph = PasswordHasher()  # Argon2id con los parámetros recomendados por la librería


def hashear_clave(clave: str) -> str:
    return ph.hash(clave)


def es_hash(clave: str) -> bool:
    return clave.startswith("$argon2")


def verificar_clave(clave_guardada: str | None, clave_ingresada: str) -> bool:
    if not clave_guardada:
        return False
    try:
        return ph.verify(clave_guardada, clave_ingresada)
    except VerifyMismatchError:
        return False
    except InvalidHashError:
        # Clave vieja guardada en texto plano: se compara directo hasta que se migre
        return clave_guardada == clave_ingresada
