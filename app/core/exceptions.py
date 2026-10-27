"""Errores de la aplicación, independientes de HTTP.

Las capas internas lanzan estos errores; `app/api/errors.py` los traduce a respuestas HTTP.
"""


class AppError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(AppError):
    """El recurso solicitado no existe."""


class ConflictError(AppError):
    """La operación choca con el estado actual (por ejemplo, un nombre duplicado)."""
