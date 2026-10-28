# Changelog

Todos los cambios relevantes de este proyecto se documentan aquí.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto sigue [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

### Added

- Torneos en `/api/v1/tournaments`: crear, listar (filtros por estado y formato), ver, editar y eliminar.
- Ciclo de vida del torneo: acciones `open-registration` y `cancel`, con reglas en
  `services/tournament_lifecycle.py` y tests unitarios.
- Inscripciones en `/api/v1/tournaments/{id}/registrations`: inscribir (con control de cupo),
  listar y desinscribir.
- Migración `add tournaments and registrations`.
- ADR-0009: ciclo de vida del torneo.

- CRUD de jugadores en `/api/v1/players`: crear, listar (paginación y búsqueda), ver, renombrar y eliminar.
- Errores de aplicación (`NotFoundError`, `ConflictError`) con manejador global → 404 / 409.
- Migración `add players table`; los tests de integración aplican las migraciones reales.
- ADR-0008: repositorios, transacciones y errores de aplicación.
- Notas didácticas en `docs/aprendizaje/`.

- PostgreSQL 17 con `docker-compose.yml` (bases `torneos` y `torneos_test`).
- SQLAlchemy 2 async: engine y sesión por petición (`SessionDep`), `Base` con convención de nombres.
- Alembic configurado para leer la URL desde `Settings`; el CI verifica las migraciones.
- ADR-0007: PostgreSQL + SQLAlchemy async + Alembic.
- Vault de Obsidian en `docs/`: arquitectura, glosario, ADRs 0001–0006, roadmap y bitácora.
- `CLAUDE.md`, skills de Claude Code (`/adr`, `/cerrar-sesion`) y política de uso de IA.
- Sección de uso de IA y ADR en la plantilla de PR.

### Changed

- Eliminar un jugador inscrito en algún torneo responde 409 (antes, error 500).

- `GET /health` reporta el estado de la base de datos y responde 503 si no está disponible.
- `create_app()` acepta un `Settings` opcional (los tests usan su propia base de datos).

## [0.1.0] - 2026-10-26

### Added

- Estructura base del proyecto con FastAPI (`app/`).
- Configuración por variables de entorno con `pydantic-settings`.
- Endpoint `GET /health`.
- Tooling de calidad: Ruff, mypy (strict), pytest con cobertura y pre-commit.
- Pipeline de CI en GitHub Actions.
