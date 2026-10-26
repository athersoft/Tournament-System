---
tags: [adr, base-de-datos]
estado: aceptado
fecha: 2026-10-26
---

# ADR-0007 PostgreSQL + SQLAlchemy 2.0 async + Alembic

## Contexto

La Fase 1 introduce persistencia: jugadores, torneos, inscripciones y partidas, con relaciones
y restricciones de integridad (un jugador no se inscribe dos veces, una partida pertenece a un torneo).
La API es asíncrona (FastAPI) y el esquema va a evolucionar en cada fase.

## Decisión

- **PostgreSQL 17** como base de datos, en desarrollo mediante `docker-compose.yml`.
- **SQLAlchemy 2.x** en modo asíncrono con el driver **asyncpg**.
- **Alembic** para migraciones versionadas; el esquema nunca se modifica a mano.
- Los **tests de integración corren contra PostgreSQL real** (base `torneos_test`), en local
  vía Docker y en CI vía *service container* de GitHub Actions.
- El engine y la fábrica de sesiones se crean en el `lifespan` de la app y se exponen con la
  dependencia `SessionDep`; la configuración llega por `Settings`, lo que permite a los tests
  apuntar a otra base sin variables globales.

## Alternativas consideradas

- **SQLite** — sin instalación, pero difiere de PostgreSQL en tipos, concurrencia y constraints;
  los errores aparecerían recién en producción.
- **SQLModel** — menos código repetido entre modelos y schemas, pero mezcla capas que
  [ADR-0003](ADR-0003-arquitectura-en-capas.md) separa a propósito, y va un paso detrás de SQLAlchemy.
- **psycopg 3** — también soporta async, pero asyncpg es más rápido y es la opción más documentada
  con SQLAlchemy async.
- **Tests con SQLite en memoria** — más rápidos, pero no prueban el motor real.

## Consecuencias

- Docker Desktop es requisito para desarrollar y correr los tests de integración en local.
- Las migraciones forman parte de cada PR que cambie modelos, y el CI verifica que se apliquen.
- `GET /health` reporta el estado de la base de datos (503 si no responde).
