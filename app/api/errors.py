from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError, ConflictError, NotFoundError

# Mismo formato que las HTTPException de FastAPI: {"detail": "..."}
_STATUS_BY_ERROR: dict[type[AppError], int] = {
    NotFoundError: status.HTTP_404_NOT_FOUND,
    ConflictError: status.HTTP_409_CONFLICT,
}


async def app_error_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, AppError)
    status_code = next(
        (code for error_type, code in _STATUS_BY_ERROR.items() if isinstance(exc, error_type)),
        status.HTTP_400_BAD_REQUEST,
    )
    return JSONResponse(status_code=status_code, content={"detail": exc.message})


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
