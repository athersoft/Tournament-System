# Changelog

Todos los cambios relevantes de este proyecto se documentan aquí.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto sigue [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

## [0.1.0] - 2026-10-26

### Added

- Estructura base del proyecto con FastAPI (`app/`).
- Configuración por variables de entorno con `pydantic-settings`.
- Endpoint `GET /health`.
- Tooling de calidad: Ruff, mypy (strict), pytest con cobertura y pre-commit.
- Pipeline de CI en GitHub Actions.
