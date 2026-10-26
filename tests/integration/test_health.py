from fastapi.testclient import TestClient

from app import __version__
from app.core.config import Settings
from app.main import create_app


def test_health_returns_ok_when_database_is_available(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "ok"
    assert body["version"] == __version__


def test_health_returns_503_when_database_is_unreachable() -> None:
    settings = Settings(
        environment="testing",
        database_url="postgresql+asyncpg://torneos:torneos@127.0.0.1:1/torneos_test",
    )

    with TestClient(create_app(settings)) as client:
        response = client.get("/health")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "degraded"
    assert body["database"] == "unavailable"
