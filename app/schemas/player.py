from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.core.constants import DEFAULT_RATING

PlayerName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


class PlayerCreate(BaseModel):
    name: PlayerName = Field(examples=["Magnus"])
    rating: int = Field(default=DEFAULT_RATING, ge=0, le=4000, description="Rating ELO inicial")


class PlayerUpdate(BaseModel):
    """El rating no se edita a mano: lo actualiza el cálculo ELO al cerrar partidas."""

    name: PlayerName | None = None


class PlayerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    rating: int
    created_at: datetime
    updated_at: datetime
