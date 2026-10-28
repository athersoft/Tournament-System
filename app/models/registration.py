from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.player import Player


class Registration(TimestampMixin, Base):
    """Inscripción de un jugador en un torneo."""

    __tablename__ = "registrations"
    __table_args__ = (UniqueConstraint("tournament_id", "player_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    # Borrar un torneo borra sus inscripciones; borrar un jugador inscrito está prohibido.
    # Sin index=True: el índice del UNIQUE (tournament_id, player_id) ya cubre tournament_id.
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id", ondelete="CASCADE"))
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="RESTRICT"), index=True
    )

    # lazy="raise": en async, una carga implícita fallaría con un error confuso.
    # Así, olvidar cargar la relación explícitamente da un error claro.
    player: Mapped[Player] = relationship(lazy="raise")
