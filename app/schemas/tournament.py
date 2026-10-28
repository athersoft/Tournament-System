from datetime import datetime
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from app.core.enums import TournamentFormat, TournamentStatus

TournamentName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]
MaxPlayers = Annotated[int, Field(ge=2, le=1024, description="Cupo; null = sin límite")]


class TournamentCreate(BaseModel):
    name: TournamentName = Field(examples=["Abierto de Primavera"])
    format: TournamentFormat
    max_players: MaxPlayers | None = None


class TournamentUpdate(BaseModel):
    """Solo los campos enviados se modifican. `max_players: null` quita el límite."""

    name: TournamentName | None = None
    format: TournamentFormat | None = None
    max_players: MaxPlayers | None = None

    @model_validator(mode="after")
    def reject_null_required_fields(self) -> Self:
        # Omitir `name` = no cambiarlo; enviarlo como null = intentar borrarlo (no permitido).
        for field in ("name", "format"):
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"'{field}' no puede ser null")
        return self


class TournamentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    format: TournamentFormat
    status: TournamentStatus
    max_players: int | None
    created_at: datetime
    updated_at: datetime
