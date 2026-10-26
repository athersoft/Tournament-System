from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from app import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Sistema de Torneos"
    app_version: str = __version__
    environment: Literal["development", "testing", "production"] = "development"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
