from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.player import PlayerRead


class RegistrationCreate(BaseModel):
    player_id: int


class RegistrationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tournament_id: int
    player: PlayerRead
    created_at: datetime
