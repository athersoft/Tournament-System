from fastapi import APIRouter, Response, status

from app.api.deps import SessionDep, SettingsDep
from app.core.database import is_database_available
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Estado del servicio",
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": HealthResponse}},
)
async def health(settings: SettingsDep, session: SessionDep, response: Response) -> HealthResponse:
    database_ok = await is_database_available(session)
    if not database_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return HealthResponse(
        status="ok" if database_ok else "degraded",
        version=settings.app_version,
        environment=settings.environment,
        database="ok" if database_ok else "unavailable",
    )
