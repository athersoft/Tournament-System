from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.integration.factories import (
    PLAYERS_URL,
    create_player,
    create_tournament,
    open_registration,
    register,
)

# --- Crear ---------------------------------------------------------------


def test_create_player_returns_201_with_default_rating(client: TestClient) -> None:
    body = create_player(client, "Magnus")

    assert body["id"] == 1
    assert body["name"] == "Magnus"
    assert body["rating"] == 1200
    assert body["created_at"] is not None


def test_create_player_strips_whitespace_and_accepts_initial_rating(client: TestClient) -> None:
    body = create_player(client, "  Hikaru  ", rating=1850)

    assert body["name"] == "Hikaru"
    assert body["rating"] == 1850


def test_create_player_returns_409_when_name_already_exists(client: TestClient) -> None:
    create_player(client, "Magnus")

    response = client.post(PLAYERS_URL, json={"name": "Magnus"})

    assert response.status_code == 409
    assert "Magnus" in response.json()["detail"]


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"name": ""},
        {"name": "   "},
        {"name": "x" * 101},
        {"name": "Magnus", "rating": -1},
        {"name": "Magnus", "rating": 4001},
    ],
)
def test_create_player_returns_422_when_payload_is_invalid(
    client: TestClient, payload: dict[str, Any]
) -> None:
    response = client.post(PLAYERS_URL, json=payload)

    assert response.status_code == 422


# --- Leer ----------------------------------------------------------------


def test_get_player_returns_player(client: TestClient) -> None:
    created = create_player(client, "Magnus")

    response = client.get(f"{PLAYERS_URL}/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_player_returns_404_when_player_does_not_exist(client: TestClient) -> None:
    response = client.get(f"{PLAYERS_URL}/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "No existe el jugador 999"}


# --- Listar --------------------------------------------------------------


def test_list_players_returns_empty_page_when_there_are_no_players(client: TestClient) -> None:
    response = client.get(PLAYERS_URL)

    assert response.status_code == 200
    assert response.json() == {"items": [], "total": 0, "limit": 20, "offset": 0}


def test_list_players_paginates_in_creation_order(client: TestClient) -> None:
    for name in ["Ana", "Beto", "Carla", "Dani", "Eva"]:
        create_player(client, name)

    response = client.get(PLAYERS_URL, params={"limit": 2, "offset": 2})

    body = response.json()
    assert [player["name"] for player in body["items"]] == ["Carla", "Dani"]
    assert body["total"] == 5
    assert body["limit"] == 2
    assert body["offset"] == 2


def test_list_players_filters_by_name_case_insensitive(client: TestClient) -> None:
    for name in ["Magnus", "Magda", "Hikaru"]:
        create_player(client, name)

    response = client.get(PLAYERS_URL, params={"search": "MAG"})

    body = response.json()
    assert [player["name"] for player in body["items"]] == ["Magnus", "Magda"]
    assert body["total"] == 2


def test_list_players_treats_wildcards_in_search_as_literal_text(client: TestClient) -> None:
    create_player(client, "Magnus")
    create_player(client, "100%_real")

    response = client.get(PLAYERS_URL, params={"search": "%"})

    assert [player["name"] for player in response.json()["items"]] == ["100%_real"]


@pytest.mark.parametrize("params", [{"limit": 0}, {"limit": 101}, {"offset": -1}])
def test_list_players_returns_422_when_pagination_is_out_of_range(
    client: TestClient, params: dict[str, int]
) -> None:
    response = client.get(PLAYERS_URL, params=params)

    assert response.status_code == 422


# --- Actualizar ----------------------------------------------------------


def test_update_player_changes_name_and_keeps_rating(client: TestClient) -> None:
    created = create_player(client, "Magnus", rating=2000)

    response = client.patch(f"{PLAYERS_URL}/{created['id']}", json={"name": "Magnus C."})

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Magnus C."
    assert body["rating"] == 2000


def test_update_player_ignores_rating_field(client: TestClient) -> None:
    created = create_player(client, "Magnus")

    response = client.patch(f"{PLAYERS_URL}/{created['id']}", json={"rating": 3000})

    assert response.status_code == 200
    assert response.json()["rating"] == 1200


def test_update_player_returns_409_when_name_belongs_to_another_player(
    client: TestClient,
) -> None:
    create_player(client, "Magnus")
    other = create_player(client, "Hikaru")

    response = client.patch(f"{PLAYERS_URL}/{other['id']}", json={"name": "Magnus"})

    assert response.status_code == 409
    assert client.get(f"{PLAYERS_URL}/{other['id']}").json()["name"] == "Hikaru"


def test_update_player_returns_404_when_player_does_not_exist(client: TestClient) -> None:
    response = client.patch(f"{PLAYERS_URL}/999", json={"name": "Nadie"})

    assert response.status_code == 404


# --- Eliminar ------------------------------------------------------------


def test_delete_player_returns_204_and_removes_player(client: TestClient) -> None:
    created = create_player(client, "Magnus")

    response = client.delete(f"{PLAYERS_URL}/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"{PLAYERS_URL}/{created['id']}").status_code == 404


def test_delete_player_returns_404_when_player_does_not_exist(client: TestClient) -> None:
    response = client.delete(f"{PLAYERS_URL}/999")

    assert response.status_code == 404


def test_delete_player_returns_409_when_player_is_registered_in_a_tournament(
    client: TestClient,
) -> None:
    player = create_player(client, "Magnus")
    tournament = create_tournament(client)
    open_registration(client, tournament["id"])
    register(client, tournament["id"], player["id"])

    response = client.delete(f"{PLAYERS_URL}/{player['id']}")

    assert response.status_code == 409
    assert client.get(f"{PLAYERS_URL}/{player['id']}").status_code == 200
