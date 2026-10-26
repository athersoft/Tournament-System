---
tags: [adr, tooling]
estado: aceptado
fecha: 2026-10-26
---

# ADR-0004 `pip` + `venv` con `pyproject.toml`

## Contexto

El proyecto necesita declarar dependencias de ejecución y de desarrollo de forma reproducible,
tanto localmente (Windows) como en CI (Linux).

## Decisión

Usaremos `pyproject.toml` (PEP 621) con backend `hatchling`, dependencias de desarrollo en el
extra `[dev]`, e instalación con `pip install -e ".[dev]"` dentro de un `venv`.

## Alternativas consideradas

- **uv** — mucho más rápido y con lockfile, pero no estaba instalado; se puede adoptar después
  sin cambiar `pyproject.toml`.
- **Poetry** — lockfile y gestión completa, pero formato propio y una herramienta más.

## Consecuencias

- Cero herramientas extra para contribuir: solo Python.
- **No hay lockfile**: las versiones pueden variar entre instalaciones. Revisar al llegar a la Fase 4
  (migrar a `uv` con `uv.lock` es la opción preferida).
