"""Reglas del ciclo de vida de un torneo.

Lógica de dominio pura: recibe estados y números, no objetos ORM ni peticiones HTTP.
Cada regla incumplida lanza `ConflictError` (409): la petición es válida, pero choca con
el estado actual del torneo.
"""

from app.core.enums import TournamentStatus
from app.core.exceptions import ConflictError

ALLOWED_TRANSITIONS: dict[TournamentStatus, frozenset[TournamentStatus]] = {
    TournamentStatus.DRAFT: frozenset({TournamentStatus.REGISTRATION, TournamentStatus.CANCELLED}),
    TournamentStatus.REGISTRATION: frozenset(
        {TournamentStatus.IN_PROGRESS, TournamentStatus.CANCELLED}
    ),
    TournamentStatus.IN_PROGRESS: frozenset({TournamentStatus.FINISHED}),
    TournamentStatus.FINISHED: frozenset(),
    TournamentStatus.CANCELLED: frozenset(),
}

EDITABLE_STATUSES = frozenset({TournamentStatus.DRAFT, TournamentStatus.REGISTRATION})
DELETABLE_STATUSES = frozenset({TournamentStatus.DRAFT, TournamentStatus.CANCELLED})


def ensure_transition(current: TournamentStatus, target: TournamentStatus) -> None:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise ConflictError(f"Un torneo en estado '{current}' no puede pasar a '{target}'")


def ensure_editable(status: TournamentStatus) -> None:
    if status not in EDITABLE_STATUSES:
        raise ConflictError(f"Un torneo en estado '{status}' ya no se puede modificar")


def ensure_format_changeable(status: TournamentStatus) -> None:
    if status is not TournamentStatus.DRAFT:
        raise ConflictError("El formato solo se puede cambiar mientras el torneo es borrador")


def ensure_deletable(status: TournamentStatus) -> None:
    if status not in DELETABLE_STATUSES:
        raise ConflictError(
            f"Un torneo en estado '{status}' no se puede eliminar; solo borradores o cancelados"
        )


def ensure_registration_open(status: TournamentStatus) -> None:
    if status is not TournamentStatus.REGISTRATION:
        raise ConflictError("Las inscripciones de este torneo no están abiertas")


def ensure_has_capacity(max_players: int | None, registered_count: int) -> None:
    """Comprueba que quepa un jugador más. `max_players=None` significa sin límite."""
    if max_players is not None and registered_count >= max_players:
        raise ConflictError(f"El torneo está completo ({max_players} jugadores)")


def ensure_capacity_not_below_registered(max_players: int | None, registered_count: int) -> None:
    if max_players is not None and max_players < registered_count:
        raise ConflictError(
            f"El cupo ({max_players}) no puede ser menor que los inscritos ({registered_count})"
        )
