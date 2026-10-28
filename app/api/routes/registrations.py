from collections.abc import Sequence

from fastapi import APIRouter, status

from app.api.deps import (
    PlayerRepositoryDep,
    RegistrationRepositoryDep,
    SessionDep,
    TournamentRepositoryDep,
)
from app.api.responses import conflict, not_found
from app.models.registration import Registration
from app.schemas.registration import RegistrationCreate, RegistrationRead
from app.services import tournament_lifecycle as lifecycle

router = APIRouter(prefix="/tournaments/{tournament_id}/registrations", tags=["registrations"])

ERROR_404 = not_found("El torneo, el jugador o la inscripción no existe")


@router.post(
    "",
    response_model=RegistrationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Inscribir jugador",
    responses={
        **ERROR_404,
        **conflict("Inscripciones cerradas, torneo completo o jugador ya inscrito"),
    },
)
async def register_player(
    tournament_id: int,
    data: RegistrationCreate,
    tournaments: TournamentRepositoryDep,
    players: PlayerRepositoryDep,
    registrations: RegistrationRepositoryDep,
    session: SessionDep,
) -> Registration:
    # FOR UPDATE: las inscripciones simultáneas al mismo torneo esperan su turno,
    # así dos personas no pueden ocupar a la vez el último cupo.
    tournament = await tournaments.get(tournament_id, for_update=True)
    lifecycle.ensure_registration_open(tournament.status)
    player = await players.get(data.player_id)
    registered = await registrations.count_by_tournament(tournament_id)
    lifecycle.ensure_has_capacity(tournament.max_players, registered)

    registration = await registrations.add(
        Registration(tournament_id=tournament_id, player_id=player.id, player=player)
    )
    await session.commit()
    return registration


@router.get("", response_model=list[RegistrationRead], summary="Listar inscritos")
async def list_registrations(
    tournament_id: int,
    tournaments: TournamentRepositoryDep,
    registrations: RegistrationRepositoryDep,
) -> Sequence[Registration]:
    await tournaments.get(tournament_id)  # 404 si el torneo no existe
    return await registrations.list_by_tournament(tournament_id)


@router.delete(
    "/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desinscribir jugador",
    responses={**ERROR_404, **conflict("Las inscripciones del torneo no están abiertas")},
)
async def unregister_player(
    tournament_id: int,
    player_id: int,
    tournaments: TournamentRepositoryDep,
    registrations: RegistrationRepositoryDep,
    session: SessionDep,
) -> None:
    tournament = await tournaments.get(tournament_id, for_update=True)
    lifecycle.ensure_registration_open(tournament.status)
    registration = await registrations.get(tournament_id, player_id)
    await registrations.delete(registration)
    await session.commit()
