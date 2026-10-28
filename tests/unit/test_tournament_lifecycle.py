import pytest

from app.core.enums import TournamentStatus as Status
from app.core.exceptions import ConflictError
from app.services import tournament_lifecycle as lifecycle

VALID_TRANSITIONS = [
    (Status.DRAFT, Status.REGISTRATION),
    (Status.DRAFT, Status.CANCELLED),
    (Status.REGISTRATION, Status.IN_PROGRESS),
    (Status.REGISTRATION, Status.CANCELLED),
    (Status.IN_PROGRESS, Status.FINISHED),
]
INVALID_TRANSITIONS = [
    (current, target)
    for current in Status
    for target in Status
    if (current, target) not in VALID_TRANSITIONS
]


# --- Transiciones ----------------------------------------------------------


@pytest.mark.parametrize(("current", "target"), VALID_TRANSITIONS)
def test_ensure_transition_allows_valid_transition(current: Status, target: Status) -> None:
    lifecycle.ensure_transition(current, target)


@pytest.mark.parametrize(("current", "target"), INVALID_TRANSITIONS)
def test_ensure_transition_rejects_invalid_transition(current: Status, target: Status) -> None:
    with pytest.raises(ConflictError):
        lifecycle.ensure_transition(current, target)


def test_transition_table_covers_every_status() -> None:
    assert set(lifecycle.ALLOWED_TRANSITIONS) == set(Status)


@pytest.mark.parametrize("status", [Status.FINISHED, Status.CANCELLED])
def test_terminal_statuses_have_no_exit(status: Status) -> None:
    assert lifecycle.ALLOWED_TRANSITIONS[status] == frozenset()


# --- Edición y borrado -----------------------------------------------------


@pytest.mark.parametrize("status", [Status.DRAFT, Status.REGISTRATION])
def test_ensure_editable_allows_draft_and_registration(status: Status) -> None:
    lifecycle.ensure_editable(status)


@pytest.mark.parametrize("status", [Status.IN_PROGRESS, Status.FINISHED, Status.CANCELLED])
def test_ensure_editable_rejects_started_or_closed_tournament(status: Status) -> None:
    with pytest.raises(ConflictError):
        lifecycle.ensure_editable(status)


def test_ensure_format_changeable_allows_only_draft() -> None:
    lifecycle.ensure_format_changeable(Status.DRAFT)
    with pytest.raises(ConflictError):
        lifecycle.ensure_format_changeable(Status.REGISTRATION)


@pytest.mark.parametrize("status", [Status.DRAFT, Status.CANCELLED])
def test_ensure_deletable_allows_draft_and_cancelled(status: Status) -> None:
    lifecycle.ensure_deletable(status)


@pytest.mark.parametrize("status", [Status.REGISTRATION, Status.IN_PROGRESS, Status.FINISHED])
def test_ensure_deletable_rejects_tournament_with_activity(status: Status) -> None:
    with pytest.raises(ConflictError):
        lifecycle.ensure_deletable(status)


# --- Inscripciones ---------------------------------------------------------


def test_ensure_registration_open_allows_only_registration_status() -> None:
    lifecycle.ensure_registration_open(Status.REGISTRATION)
    for status in set(Status) - {Status.REGISTRATION}:
        with pytest.raises(ConflictError):
            lifecycle.ensure_registration_open(status)


@pytest.mark.parametrize(
    ("max_players", "registered"),
    [(None, 0), (None, 10_000), (8, 0), (8, 7)],
)
def test_ensure_has_capacity_allows_when_there_is_room(
    max_players: int | None, registered: int
) -> None:
    lifecycle.ensure_has_capacity(max_players, registered)


@pytest.mark.parametrize(("max_players", "registered"), [(8, 8), (2, 2), (8, 9)])
def test_ensure_has_capacity_rejects_when_full(max_players: int, registered: int) -> None:
    with pytest.raises(ConflictError, match="completo"):
        lifecycle.ensure_has_capacity(max_players, registered)


@pytest.mark.parametrize(("max_players", "registered"), [(None, 5), (5, 5), (8, 5)])
def test_ensure_capacity_not_below_registered_allows_equal_or_higher(
    max_players: int | None, registered: int
) -> None:
    lifecycle.ensure_capacity_not_below_registered(max_players, registered)


def test_ensure_capacity_not_below_registered_rejects_lower_capacity() -> None:
    with pytest.raises(ConflictError):
        lifecycle.ensure_capacity_not_below_registered(4, 5)
