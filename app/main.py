from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import health
from app.core.config import Settings, get_settings
from app.core.database import create_engine, create_sessionmaker


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = create_engine(settings)
        app.state.sessionmaker = create_sessionmaker(engine)
        yield
        await engine.dispose()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )
    app.state.settings = settings
    app.include_router(health.router)
    return app


app = create_app()
