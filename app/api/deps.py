from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import Settings
from app.repositories.player_repository import PlayerRepository
from app.repositories.registration_repository import RegistrationRepository
from app.repositories.tournament_repository import TournamentRepository


def get_app_settings(request: Request) -> Settings:
    settings: Settings = request.app.state.settings
    return settings


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    sessionmaker: async_sessionmaker[AsyncSession] = request.app.state.sessionmaker
    async with sessionmaker() as session:
        yield session


SettingsDep = Annotated[Settings, Depends(get_app_settings)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_player_repository(session: SessionDep) -> PlayerRepository:
    return PlayerRepository(session)


def get_tournament_repository(session: SessionDep) -> TournamentRepository:
    return TournamentRepository(session)


def get_registration_repository(session: SessionDep) -> RegistrationRepository:
    return RegistrationRepository(session)


PlayerRepositoryDep = Annotated[PlayerRepository, Depends(get_player_repository)]
TournamentRepositoryDep = Annotated[TournamentRepository, Depends(get_tournament_repository)]
RegistrationRepositoryDep = Annotated[RegistrationRepository, Depends(get_registration_repository)]
