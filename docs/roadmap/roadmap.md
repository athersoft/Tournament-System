---
tags: [roadmap]
fase_actual: 1
actualizado: 2026-10-27
---

# Roadmap

Cada fase corresponde a un **milestone de GitHub** y termina en una release etiquetada.

## ✅ Fase 0 — Fundaciones del repositorio · `v0.1.0`

- [x] Estructura `app/` en capas y nombres en snake_case
- [x] `pyproject.toml` con Ruff, mypy (strict), pytest y cobertura mínima 80%
- [x] pre-commit y CI en GitHub Actions (Python 3.11 y 3.12)
- [x] `GET /health` con test
- [x] README, CHANGELOG, LICENSE, plantillas de PR e issues
- [x] Repositorio publicado en GitHub
- [x] Tag `v0.1.0`
- [x] Protección de rama `main` (PR + CI obligatorios)
- [x] Vault de Obsidian y configuración de IA (`CLAUDE.md`, `.claude/`)

## ⏳ Fase 1 — Núcleo de datos · `v0.2.0`

- [x] ADR: PostgreSQL + SQLAlchemy 2.0 async + Alembic ([ADR-0007](../decisiones/ADR-0007-postgresql-sqlalchemy.md))
- [x] `core/database.py` (engine y sesión async) + docker-compose con PostgreSQL
- [x] Alembic configurado + verificación de migraciones en CI
- [x] Modelo `Player` + migración + CRUD `/api/v1/players` (paginación, búsqueda) — PR #3
- [x] Repositorios y manejo de errores consistente (404, 409, 422) ([ADR-0008](../decisiones/ADR-0008-repositorios-y-errores.md))
- [x] Tests de integración con BD aislada (migraciones reales + `TRUNCATE` por test)
- [ ] Modelos `Tournament` y `Registration` + CRUD de torneos e inscripciones
- [ ] Modelo `Match` (sin lógica de rondas todavía)
- [ ] Revisar aviso de Starlette sobre `httpx` en `TestClient`

## Fase 2 — Lógica de torneos · `v0.3.0`

- [ ] Eliminación directa: seeding, byes, avance de ronda
- [ ] Sistema suizo: emparejamiento por puntaje sin repetir rival, Buchholz, Sonneborn-Berger
- [ ] Round robin (algoritmo del círculo)
- [ ] ELO con factor K configurable
- [ ] Máquina de estados del torneo
- [ ] Endpoints `start`, `result`, `standings`, `bracket`

## Fase 3 — Autenticación y permisos · `v0.4.0`

- [ ] JWT (access + refresh), roles `admin` / `organizer` / `player`
- [ ] Reglas de autorización por recurso

## Fase 4 — Calidad de producción · `v0.5.0`

- [ ] Dockerfile multi-stage, logging estructurado, manejo global de errores
- [ ] CORS, rate limiting (versionado `/api/v1` ya adelantado en Fase 1)
- [ ] Lockfile (evaluar `uv`, ver ADR-0004)

## Fase 5 — Deploy y presentación · `v1.0.0`

- [ ] Deploy automático + BD gestionada
- [ ] README final con badges, diagramas y demo en vivo
