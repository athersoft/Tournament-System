"""Modelos ORM. Importar aquí cada modelo para que Alembic los detecte."""

from app.models.base import Base
from app.models.player import Player

__all__ = ["Base", "Player"]
