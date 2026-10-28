from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.deps import RegistrationRepositoryDep, SessionDep, TournamentRepositoryDep
from app.api.responses import conflict, not_found
from app.core.enums import TournamentFormat, TournamentStatus
from app.models.tournament import Tournament
from app.schemas.pagination import Page
from app.schemas.tournament import TournamentCreate, TournamentRead, TournamentUpdate
from app.services import tournament_lifecycle as lifecycle

router = APIRouter(prefix="/tournaments", tags=["tournaments"])

ERROR_404 = not_found("El torneo no existe")
ERROR_409 = conflict("La operación no está permitida en el estado actual del torneo")


@router.post(
    "", response_model=TournamentRead, status_code=status.HTTP_201_CREATED, summary="Crear torneo"
)
async def create_tournament(
    data: TournamentCreate, tournaments: TournamentRepositoryDep, session: SessionDep
) -> Tournament:
    tournament = await tournaments.save(Tournament(**data.model_dump()))
    await session.commit()
    return tournament


@router.get("", response_model=Page[TournamentRead], summary="Listar torneos")
async def list_tournaments(
    tournaments: TournamentRepositoryDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    status_filter: Annotated[TournamentStatus | None, Query(alias="status")] = None,
    format_filter: Annotated[TournamentFormat | None, Query(alias="format")] = None,
) -> Page[TournamentRead]:
    items, total = await tournaments.paginate(
        limit=limit, offset=offset, status=status_filter, format=format_filter
    )
    return Page[TournamentRead](
        items=[TournamentRead.model_validate(tournament) for tournament in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{tournament_id}", response_model=TournamentRead, summary="Ver torneo", responses=ERROR_404
)
async def get_tournament(tournament_id: int, tournaments: TournamentRepositoryDep) -> Tournament:
    return await tournaments.get(tournament_id)


@router.patch(
    "/{tournament_id}",
    response_model=TournamentRead,
    summary="Actualizar torneo",
    description=(
        "Solo en borrador o con inscripciones abiertas. El formato solo cambia en borrador "
        "y el cupo no puede quedar por debajo de los inscritos."
    ),
    responses={**ERROR_404, **ERROR_409},
)
async def update_tournament(
    tournament_id: int,
    data: TournamentUpdate,
    tournaments: TournamentRepositoryDep,
    registrations: RegistrationRepositoryDep,
    session: SessionDep,
) -> Tournament:
    tournament = await tournaments.get(tournament_id, for_update=True)
    lifecycle.ensure_editable(tournament.status)

    changes = data.model_dump(exclude_unset=True)
    if changes.get("format", tournament.format) != tournament.format:
        lifecycle.ensure_format_changeable(tournament.status)
    if "max_players" in changes:
        registered = await registrations.count_by_tournament(tournament_id)
        lifecycle.ensure_capacity_not_below_registered(changes["max_players"], registered)

    for field, value in changes.items():
        setattr(tournament, field, value)
    await tournaments.save(tournament)
    await session.commit()
    return tournament


@router.delete(
    "/{tournament_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar torneo",
    description="Solo borradores o torneos cancelados; el resto se conserva como historial.",
    responses={**ERROR_404, **ERROR_409},
)
async def delete_tournament(
    tournament_id: int, tournaments: TournamentRepositoryDep, session: SessionDep
) -> None:
    tournament = await tournaments.get(tournament_id)
    lifecycle.ensure_deletable(tournament.status)
    await tournaments.delete(tournament)
    await session.commit()


# --- Acciones del ciclo de vida --------------------------------------------


async def _transition(
    tournament_id: int,
    target: TournamentStatus,
    tournaments: TournamentRepositoryDep,
    session: SessionDep,
) -> Tournament:
    tournament = await tournaments.get(tournament_id, for_update=True)
    lifecycle.ensure_transition(tournament.status, target)
    tournament.status = target
    await tournaments.save(tournament)
    await session.commit()
    return tournament


@router.post(
    "/{tournament_id}/open-registration",
    response_model=TournamentRead,
    summary="Abrir inscripciones",
    description="Borrador → inscripciones abiertas.",
    responses={**ERROR_404, **ERROR_409},
)
async def open_registration(
    tournament_id: int, tournaments: TournamentRepositoryDep, session: SessionDep
) -> Tournament:
    return await _transition(tournament_id, TournamentStatus.REGISTRATION, tournaments, session)


@router.post(
    "/{tournament_id}/cancel",
    response_model=TournamentRead,
    summary="Cancelar torneo",
    description="Desde borrador o inscripciones abiertas. Un torneo cancelado no se reabre.",
    responses={**ERROR_404, **ERROR_409},
)
async def cancel_tournament(
    tournament_id: int, tournaments: TournamentRepositoryDep, session: SessionDep
) -> Tournament:
    return await _transition(tournament_id, TournamentStatus.CANCELLED, tournaments, session)
