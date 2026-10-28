"""Respuestas de error documentadas en OpenAPI (/docs), reutilizables entre rutas."""

from typing import Any

from fastapi import status

Responses = dict[int | str, dict[str, Any]]


def not_found(description: str) -> Responses:
    return {status.HTTP_404_NOT_FOUND: {"description": description}}


def conflict(description: str) -> Responses:
    return {status.HTTP_409_CONFLICT: {"description": description}}
