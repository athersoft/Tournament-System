from enum import StrEnum

from sqlalchemy import CheckConstraint, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import TournamentFormat, TournamentStatus
from app.models.base import Base, TimestampMixin


def _string_enum(enum_class: type[StrEnum], name: str) -> Enum:
    """Enum guardado como VARCHAR + CHECK, con los valores en minúscula ('draft', no 'DRAFT').

    Se evita el ENUM nativo de PostgreSQL: agregarle valores en una migración es incómodo.
    """
    return Enum(
        enum_class,
        name=name,
        native_enum=False,
        create_constraint=True,
        length=30,
        values_callable=lambda members: [member.value for member in members],
    )


class Tournament(TimestampMixin, Base):
    __tablename__ = "tournaments"
    __table_args__ = (CheckConstraint("max_players >= 2", name="max_players_min"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    format: Mapped[TournamentFormat] = mapped_column(
        _string_enum(TournamentFormat, "tournament_format")
    )
    status: Mapped[TournamentStatus] = mapped_column(
        _string_enum(TournamentStatus, "tournament_status"),
        default=TournamentStatus.DRAFT,
        server_default=TournamentStatus.DRAFT.value,
        index=True,
    )
    max_players: Mapped[int | None]
