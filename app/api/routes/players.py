from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.deps import PlayerRepositoryDep, SessionDep
from app.api.responses import conflict, not_found
from app.models.player import Player
from app.schemas.pagination import Page
from app.schemas.player import PlayerCreate, PlayerRead, PlayerUpdate

router = APIRouter(prefix="/players", tags=["players"])

ERROR_404 = not_found("El jugador no existe")
ERROR_409 = conflict("Ya existe un jugador con ese nombre")


@router.post(
    "",
    response_model=PlayerRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear jugador",
    responses=ERROR_409,
)
async def create_player(
    data: PlayerCreate, repo: PlayerRepositoryDep, session: SessionDep
) -> Player:
    player = await repo.save(Player(name=data.name, rating=data.rating))
    await session.commit()
    return player


@router.get("", response_model=Page[PlayerRead], summary="Listar jugadores")
async def list_players(
    repo: PlayerRepositoryDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    search: Annotated[str | None, Query(max_length=100, description="Filtra por nombre")] = None,
) -> Page[PlayerRead]:
    players, total = await repo.paginate(limit=limit, offset=offset, search=search)
    return Page[PlayerRead](
        items=[PlayerRead.model_validate(player) for player in players],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{player_id}", response_model=PlayerRead, summary="Ver jugador", responses=ERROR_404)
async def get_player(player_id: int, repo: PlayerRepositoryDep) -> Player:
    return await repo.get(player_id)


@router.patch(
    "/{player_id}",
    response_model=PlayerRead,
    summary="Actualizar jugador",
    responses={**ERROR_404, **ERROR_409},
)
async def update_player(
    player_id: int, data: PlayerUpdate, repo: PlayerRepositoryDep, session: SessionDep
) -> Player:
    player = await repo.get(player_id)
    if data.name is not None:
        player.name = data.name
    await repo.save(player)
    await session.commit()
    return player


@router.delete(
    "/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar jugador",
    responses={**ERROR_404, **conflict("El jugador está inscrito en algún torneo")},
)
async def delete_player(player_id: int, repo: PlayerRepositoryDep, session: SessionDep) -> None:
    player = await repo.get(player_id)
    await repo.delete(player)
    await session.commit()
