import asyncio
import os
from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import pool, text
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import command
from app.core.config import Settings
from app.main import create_app
from app.models import Base

# Los tests nunca usan la base de desarrollo: TEST_DATABASE_URL o la base torneos_test local.
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://torneos:torneos@localhost:5432/torneos_test",
)
ALEMBIC_INI = Path(__file__).resolve().parents[2] / "alembic.ini"


@pytest.fixture(scope="session")
def migrated_database() -> None:
    """Aplica las migraciones una vez por sesión: los tests también las validan."""
    config = Config(ALEMBIC_INI)
    config.attributes["database_url"] = TEST_DATABASE_URL
    command.upgrade(config, "head")


async def _truncate_all_tables() -> None:
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=pool.NullPool)
    tables = ", ".join(table.name for table in Base.metadata.sorted_tables)
    async with engine.begin() as connection:
        await connection.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))
    await engine.dispose()


@pytest.fixture
def clean_database(migrated_database: None) -> None:
    """Cada test empieza con las tablas vacías, sin depender del orden de ejecución."""
    asyncio.run(_truncate_all_tables())


@pytest.fixture
def settings() -> Settings:
    return Settings(environment="testing", database_url=TEST_DATABASE_URL)


@pytest.fixture
def client(settings: Settings, clean_database: None) -> Iterator[TestClient]:
    with TestClient(create_app(settings)) as test_client:
        yield test_client
