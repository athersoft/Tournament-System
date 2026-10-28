from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.exceptions import ConflictError, NotFoundError
from app.models.registration import Registration


class RegistrationRepository:
    """Acceso a datos de inscripciones. No hace commit: eso lo decide quien llama."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, tournament_id: int, player_id: int) -> Registration:
        registration = await self.session.scalar(
            select(Registration).where(
                Registration.tournament_id == tournament_id,
                Registration.player_id == player_id,
            )
        )
        if registration is None:
            raise NotFoundError(
                f"El jugador {player_id} no está inscrito en el torneo {tournament_id}"
            )
        return registration

    async def list_by_tournament(self, tournament_id: int) -> Sequence[Registration]:
        """Inscripciones en orden de llegada, con el jugador cargado en la misma consulta."""
        registrations = await self.session.scalars(
            select(Registration)
            .options(joinedload(Registration.player))
            .where(Registration.tournament_id == tournament_id)
            .order_by(Registration.id)
        )
        return registrations.all()

    async def count_by_tournament(self, tournament_id: int) -> int:
        count = await self.session.scalar(
            select(func.count()).where(Registration.tournament_id == tournament_id)
        )
        return count or 0

    async def add(self, registration: Registration) -> Registration:
        tournament_id, player_id = registration.tournament_id, registration.player_id
        self.session.add(registration)
        try:
            await self.session.flush()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError(
                f"El jugador {player_id} ya está inscrito en el torneo {tournament_id}"
            ) from exc
        return registration

    async def delete(self, registration: Registration) -> None:
        await self.session.delete(registration)
        await self.session.flush()
