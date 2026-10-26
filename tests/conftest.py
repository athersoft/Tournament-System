import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app

# Los tests nunca usan la base de desarrollo: TEST_DATABASE_URL o la base torneos_test local.
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://torneos:torneos@localhost:5432/torneos_test",
)


@pytest.fixture
def settings() -> Settings:
    return Settings(environment="testing", database_url=TEST_DATABASE_URL)


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    with TestClient(create_app(settings)) as test_client:
        yield test_client
