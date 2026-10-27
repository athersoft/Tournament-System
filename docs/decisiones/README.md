---
tags: [adr, indice]
---

# Registro de decisiones (ADR)

Cada decisión técnica relevante se documenta como un *Architecture Decision Record*.
Un ADR no se edita para cambiar su decisión: se crea uno nuevo que lo **reemplaza**
y el anterior pasa a estado `reemplazado`.

Estados: `propuesto` · `aceptado` · `rechazado` · `reemplazado`

| # | Decisión | Estado |
|---|---|---|
| [0001](ADR-0001-registrar-decisiones.md) | Registrar decisiones con ADRs | aceptado |
| [0002](ADR-0002-fastapi-pydantic.md) | FastAPI + Pydantic v2 como framework | aceptado |
| [0003](ADR-0003-arquitectura-en-capas.md) | Arquitectura en capas con lógica de dominio pura | aceptado |
| [0004](ADR-0004-gestion-dependencias.md) | `pip` + `venv` con `pyproject.toml` | aceptado |
| [0005](ADR-0005-obsidian-docs.md) | Documentación como vault de Obsidian en `docs/` | aceptado |
| [0006](ADR-0006-uso-de-ia.md) | Desarrollo asistido por IA con contexto versionado | aceptado |
| [0007](ADR-0007-postgresql-sqlalchemy.md) | PostgreSQL + SQLAlchemy 2.0 async + Alembic | aceptado |
| [0008](ADR-0008-repositorios-y-errores.md) | Repositorios, transacciones y errores de aplicación | aceptado |

Plantilla: [plantillas/adr.md](../plantillas/adr.md)
