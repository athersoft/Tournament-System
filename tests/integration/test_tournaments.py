from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.integration.factories import (
    TOURNAMENTS_URL,
    cancel,
    create_player,
    create_tournament,
    open_registration,
    register,
)

# --- Crear y leer --------------------------------------------------------


def test_create_tournament_starts_as_draft(client: TestClient) -> None:
    body = create_tournament(client, "Abierto de Primavera", "single_elimination", max_players=8)

    assert body["id"] == 1
    assert body["name"] == "Abierto de Primavera"
    assert body["format"] == "single_elimination"
    assert body["status"] == "draft"
    assert body["max_players"] == 8


def test_create_tournament_without_max_players_has_no_limit(client: TestClient) -> None:
    assert create_tournament(client)["max_players"] is None


@pytest.mark.parametrize(
    "payload",
    [
        {"format": "swiss"},
        {"name": "Abierto"},
        {"name": "Abierto", "format": "poker"},
        {"name": "  ", "format": "swiss"},
        {"name": "Abierto", "format": "swiss", "max_players": 1},
    ],
)
def test_create_tournament_returns_422_when_payload_is_invalid(
    client: TestClient, payload: dict[str, Any]
) -> None:
    response = client.post(TOURNAMENTS_URL, json=payload)

    assert response.status_code == 422


def test_create_tournament_ignores_status_sent_by_client(client: TestClient) -> None:
    # `status` no es un campo de entrada: solo cambia con las acciones del ciclo de vida.
    body = create_tournament(client, status="finished")

    assert body["status"] == "draft"


def test_get_tournament_returns_404_when_tournament_does_not_exist(client: TestClient) -> None:
    response = client.get(f"{TOURNAMENTS_URL}/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "No existe el torneo 999"}


def test_list_tournaments_filters_by_status_and_format(client: TestClient) -> None:
    swiss_open = create_tournament(client, "Suizo abierto", "swiss")
    create_tournament(client, "Suizo borrador", "swiss")
    create_tournament(client, "Eliminación", "single_elimination")
    open_registration(client, swiss_open["id"])

    by_format = client.get(TOURNAMENTS_URL, params={"format": "swiss"}).json()
    by_both = client.get(TOURNAMENTS_URL, params={"format": "swiss", "status": "draft"}).json()

    assert by_format["total"] == 2
    assert [t["name"] for t in by_both["items"]] == ["Suizo borrador"]


def test_list_tournaments_returns_422_when_filter_value_is_unknown(client: TestClient) -> None:
    assert client.get(TOURNAMENTS_URL, params={"status": "paused"}).status_code == 422


# --- Ciclo de vida -------------------------------------------------------


def test_open_registration_moves_draft_to_registration(client: TestClient) -> None:
    tournament = create_tournament(client)

    response = client.post(f"{TOURNAMENTS_URL}/{tournament['id']}/open-registration")

    assert response.status_code == 200
    assert response.json()["status"] == "registration"


def test_open_registration_returns_409_when_already_open(client: TestClient) -> None:
    tournament = create_tournament(client)
    open_registration(client, tournament["id"])

    response = client.post(f"{TOURNAMENTS_URL}/{tournament['id']}/open-registration")

    assert response.status_code == 409


def test_cancel_returns_409_when_tournament_is_already_cancelled(client: TestClient) -> None:
    tournament = create_tournament(client)
    cancel(client, tournament["id"])

    response = client.post(f"{TOURNAMENTS_URL}/{tournament['id']}/cancel")

    assert response.status_code == 409
    assert "cancelled" in response.json()["detail"]


def test_lifecycle_action_returns_404_when_tournament_does_not_exist(client: TestClient) -> None:
    assert client.post(f"{TOURNAMENTS_URL}/999/cancel").status_code == 404


# --- Actualizar ----------------------------------------------------------


def test_update_tournament_changes_only_sent_fields(client: TestClient) -> None:
    tournament = create_tournament(client, "Abierto", "swiss", max_players=8)

    response = client.patch(f"{TOURNAMENTS_URL}/{tournament['id']}", json={"name": "Cerrado"})

    body = response.json()
    assert response.status_code == 200
    assert body["name"] == "Cerrado"
    assert body["format"] == "swiss"
    assert body["max_players"] == 8


def test_update_tournament_with_null_max_players_removes_limit(client: TestClient) -> None:
    tournament = create_tournament(client, max_players=8)

    response = client.patch(f"{TOURNAMENTS_URL}/{tournament['id']}", json={"max_players": None})

    assert response.json()["max_players"] is None


@pytest.mark.parametrize("field", ["name", "format"])
def test_update_tournament_returns_422_when_required_field_is_null(
    client: TestClient, field: str
) -> None:
    tournament = create_tournament(client)

    response = client.patch(f"{TOURNAMENTS_URL}/{tournament['id']}", json={field: None})

    assert response.status_code == 422


def test_update_tournament_allows_format_change_only_in_draft(client: TestClient) -> None:
    tournament = create_tournament(client, format="swiss")
    url = f"{TOURNAMENTS_URL}/{tournament['id']}"

    assert client.patch(url, json={"format": "round_robin"}).status_code == 200
    open_registration(client, tournament["id"])
    assert client.patch(url, json={"format": "swiss"}).status_code == 409
    # Reenviar el mismo formato no es un cambio: se permite.
    assert client.patch(url, json={"format": "round_robin", "name": "X"}).status_code == 200


def test_update_tournament_returns_409_when_capacity_is_below_registered(
    client: TestClient,
) -> None:
    tournament = create_tournament(client, max_players=8)
    open_registration(client, tournament["id"])
    for name in ["Ana", "Beto", "Carla"]:
        register(client, tournament["id"], create_player(client, name)["id"])
    url = f"{TOURNAMENTS_URL}/{tournament['id']}"

    assert client.patch(url, json={"max_players": 2}).status_code == 409
    assert client.patch(url, json={"max_players": 3}).status_code == 200


def test_update_tournament_returns_409_when_tournament_is_cancelled(client: TestClient) -> None:
    tournament = create_tournament(client)
    cancel(client, tournament["id"])

    response = client.patch(f"{TOURNAMENTS_URL}/{tournament['id']}", json={"name": "Otro"})

    assert response.status_code == 409


# --- Eliminar ------------------------------------------------------------


def test_delete_tournament_removes_draft(client: TestClient) -> None:
    tournament = create_tournament(client)

    assert client.delete(f"{TOURNAMENTS_URL}/{tournament['id']}").status_code == 204
    assert client.get(f"{TOURNAMENTS_URL}/{tournament['id']}").status_code == 404


def test_delete_tournament_returns_409_when_registration_is_open(client: TestClient) -> None:
    tournament = create_tournament(client)
    open_registration(client, tournament["id"])

    assert client.delete(f"{TOURNAMENTS_URL}/{tournament['id']}").status_code == 409


def test_delete_cancelled_tournament_also_deletes_its_registrations(client: TestClient) -> None:
    player = create_player(client, "Magnus")
    tournament = create_tournament(client)
    open_registration(client, tournament["id"])
    register(client, tournament["id"], player["id"])
    cancel(client, tournament["id"])

    assert client.delete(f"{TOURNAMENTS_URL}/{tournament['id']}").status_code == 204
    # Sin inscripciones colgando (ON DELETE CASCADE), el jugador ya se puede borrar.
    assert client.delete(f"/api/v1/players/{player['id']}").status_code == 204
