"""Atajos para crear datos de prueba a través de la API (igual que lo haría un cliente)."""

from typing import Any

from fastapi.testclient import TestClient

PLAYERS_URL = "/api/v1/players"
TOURNAMENTS_URL = "/api/v1/tournaments"


def create_player(client: TestClient, name: str, **extra: Any) -> dict[str, Any]:
    response = client.post(PLAYERS_URL, json={"name": name, **extra})
    assert response.status_code == 201, response.text
    body: dict[str, Any] = response.json()
    return body


def create_tournament(
    client: TestClient, name: str = "Abierto", format: str = "swiss", **extra: Any
) -> dict[str, Any]:
    response = client.post(TOURNAMENTS_URL, json={"name": name, "format": format, **extra})
    assert response.status_code == 201, response.text
    body: dict[str, Any] = response.json()
    return body


def open_registration(client: TestClient, tournament_id: int) -> None:
    response = client.post(f"{TOURNAMENTS_URL}/{tournament_id}/open-registration")
    assert response.status_code == 200, response.text


def cancel(client: TestClient, tournament_id: int) -> None:
    response = client.post(f"{TOURNAMENTS_URL}/{tournament_id}/cancel")
    assert response.status_code == 200, response.text


def register(client: TestClient, tournament_id: int, player_id: int) -> dict[str, Any]:
    response = client.post(
        f"{TOURNAMENTS_URL}/{tournament_id}/registrations", json={"player_id": player_id}
    )
    assert response.status_code == 201, response.text
    body: dict[str, Any] = response.json()
    return body
