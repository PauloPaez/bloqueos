class EscuelaValidationError(Exception):
    """Error producido por datos inválidos o reglas de negocio de escuelas."""


class EscuelaNotFoundError(Exception):
    """Error producido cuando no existe la escuela solicitada."""
