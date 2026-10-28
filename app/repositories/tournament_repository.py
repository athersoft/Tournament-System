from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import TournamentFormat, TournamentStatus
from app.core.exceptions import NotFoundError
from app.models.tournament import Tournament


class TournamentRepository:
    """Acceso a datos de torneos. No hace commit: eso lo decide quien llama."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, tournament_id: int, *, for_update: bool = False) -> Tournament:
        """Con `for_update=True` bloquea la fila hasta el commit (SELECT ... FOR UPDATE).

        Sirve para operaciones que leen y luego deciden, como "¿queda cupo?": dos peticiones
        simultáneas se ejecutan una después de la otra en vez de ver ambas el mismo cupo libre.
        """
        query = select(Tournament).where(Tournament.id == tournament_id)
        if for_update:
            query = query.with_for_update()
        tournament = await self.session.scalar(query)
        if tournament is None:
            raise NotFoundError(f"No existe el torneo {tournament_id}")
        return tournament

    async def paginate(
        self,
        *,
        limit: int,
        offset: int,
        status: TournamentStatus | None = None,
        format: TournamentFormat | None = None,
    ) -> tuple[Sequence[Tournament], int]:
        query = select(Tournament)
        if status is not None:
            query = query.where(Tournament.status == status)
        if format is not None:
            query = query.where(Tournament.format == format)

        total = await self.session.scalar(select(func.count()).select_from(query.subquery()))
        tournaments = await self.session.scalars(
            query.order_by(Tournament.id).limit(limit).offset(offset)
        )
        return tournaments.all(), total or 0

    async def save(self, tournament: Tournament) -> Tournament:
        self.session.add(tournament)
        await self.session.flush()
        return tournament

    async def delete(self, tournament: Tournament) -> None:
        await self.session.delete(tournament)
        await self.session.flush()
