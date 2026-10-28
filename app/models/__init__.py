"""Modelos ORM. Importar aquí cada modelo para que Alembic los detecte."""

from app.models.base import Base
from app.models.player import Player
from app.models.registration import Registration
from app.models.tournament import Tournament

__all__ = ["Base", "Player", "Registration", "Tournament"]
