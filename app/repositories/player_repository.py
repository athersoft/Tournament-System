from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.player import Player


class PlayerRepository:
    """Acceso a datos de jugadores. No hace commit: eso lo decide quien llama."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, player_id: int) -> Player:
        player = await self.session.get(Player, player_id)
        if player is None:
            raise NotFoundError(f"No existe el jugador {player_id}")
        return player

    async def paginate(
        self, *, limit: int, offset: int, search: str | None = None
    ) -> tuple[Sequence[Player], int]:
        query = select(Player)
        if search:
            query = query.where(Player.name.icontains(search, autoescape=True))

        total = await self.session.scalar(select(func.count()).select_from(query.subquery()))
        players = await self.session.scalars(query.order_by(Player.id).limit(limit).offset(offset))
        return players.all(), total or 0

    async def save(self, player: Player) -> Player:
        """Inserta o actualiza el jugador y detecta nombres duplicados de inmediato."""
        name = player.name  # tras el rollback el objeto expira y no se puede leer
        self.session.add(player)
        try:
            await self.session.flush()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError(f"Ya existe un jugador llamado '{name}'") from exc
        return player

    async def delete(self, player: Player) -> None:
        await self.session.delete(player)
        await self.session.flush()
