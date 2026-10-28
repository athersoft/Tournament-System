from fastapi.testclient import TestClient

from tests.integration.factories import (
    TOURNAMENTS_URL,
    cancel,
    create_player,
    create_tournament,
    open_registration,
    register,
)


def registrations_url(tournament_id: int) -> str:
    return f"{TOURNAMENTS_URL}/{tournament_id}/registrations"


# --- Inscribir -----------------------------------------------------------


def test_register_player_returns_registration_with_player(client: TestClient) -> None:
    player = create_player(client, "Magnus", rating=2800)
    tournament = create_tournament(client)
    open_registration(client, tournament["id"])

    body = register(client, tournament["id"], player["id"])

    assert body["tournament_id"] == tournament["id"]
    assert body["player"]["name"] == "Magnus"
    assert body["player"]["rating"] == 2800


def test_register_player_returns_409_when_registration_is_not_open(client: TestClient) -> None:
    player = create_player(client, "Magnus")
    tournament = create_tournament(client)  # sigue en borrador

    response = client.post(registrations_url(tournament["id"]), json={"player_id": player["id"]})

    assert response.status_code == 409
    assert response.json()["detail"] == "Las inscripciones de este torneo no están abiertas"


def test_register_player_returns_409_when_player_is_already_registered(
    client: TestClient,
) -> None:
    player = create_player(client, "Magnus")
    tournament = create_tournament(client)
    open_registration(client, tournament["id"])
    register(client, tournament["id"], player["id"])

    response = client.post(registrations_url(tournament["id"]), json={"player_id": player["id"]})

    assert response.status_code == 409
    assert "ya está inscrito" in response.json()["detail"]


def test_register_player_returns_409_when_tournament_is_full(client: TestClient) -> None:
    tournament = create_tournament(client, max_players=2)
    open_registration(client, tournament["id"])
    for name in ["Ana", "Beto"]:
        register(client, tournament["id"], create_player(client, name)["id"])
    late = create_player(client, "Carla")

    response = client.post(registrations_url(tournament["id"]), json={"player_id": late["id"]})

    assert response.status_code == 409
    assert "completo" in response.json()["detail"]


def test_register_player_returns_404_when_player_does_not_exist(client: TestClient) -> None:
    tournament = create_tournament(client)
    open_registration(client, tournament["id"])

    response = client.post(registrations_url(tournament["id"]), json={"player_id": 999})

    assert response.status_code == 404
    assert response.json() == {"detail": "No existe el jugador 999"}


def test_register_player_returns_404_when_tournament_does_not_exist(client: TestClient) -> None:
    player = create_player(client, "Magnus")

    response = client.post(registrations_url(999), json={"player_id": player["id"]})

    assert response.status_code == 404


def test_same_player_can_register_in_different_tournaments(client: TestClient) -> None:
    player = create_player(client, "Magnus")
    for name in ["Primavera", "Otoño"]:
        tournament = create_tournament(client, name)
        open_registration(client, tournament["id"])
        register(client, tournament["id"], player["id"])


# --- Listar --------------------------------------------------------------


def test_list_registrations_returns_players_in_registration_order(client: TestClient) -> None:
    tournament = create_tournament(client)
    open_registration(client, tournament["id"])
    for name in ["Carla", "Ana", "Beto"]:
        register(client, tournament["id"], create_player(client, name)["id"])

    response = client.get(registrations_url(tournament["id"]))

    assert response.status_code == 200
    assert [r["player"]["name"] for r in response.json()] == ["Carla", "Ana", "Beto"]


def test_list_registrations_returns_404_when_tournament_does_not_exist(client: TestClient) -> None:
    assert client.get(registrations_url(999)).status_code == 404


# --- Desinscribir --------------------------------------------------------


def test_unregister_player_frees_the_spot(client: TestClient) -> None:
    tournament = create_tournament(client, max_players=2)
    open_registration(client, tournament["id"])
    ana, beto, carla = (create_player(client, name) for name in ["Ana", "Beto", "Carla"])
    register(client, tournament["id"], ana["id"])
    register(client, tournament["id"], beto["id"])

    response = client.delete(f"{registrations_url(tournament['id'])}/{ana['id']}")

    assert response.status_code == 204
    register(client, tournament["id"], carla["id"])  # el cupo quedó libre


def test_unregister_player_returns_404_when_player_is_not_registered(client: TestClient) -> None:
    tournament = create_tournament(client)
    open_registration(client, tournament["id"])

    assert client.delete(f"{registrations_url(tournament['id'])}/999").status_code == 404


def test_unregister_player_returns_409_when_registration_is_closed(client: TestClient) -> None:
    player = create_player(client, "Magnus")
    tournament = create_tournament(client)
    open_registration(client, tournament["id"])
    register(client, tournament["id"], player["id"])
    cancel(client, tournament["id"])

    response = client.delete(f"{registrations_url(tournament['id'])}/{player['id']}")

    assert response.status_code == 409
