---
tags: [adr, arquitectura]
estado: aceptado
fecha: 2026-10-26
---

# ADR-0003 Arquitectura en capas con lógica de dominio pura

## Contexto

El valor central del proyecto son los algoritmos de torneo (brackets, sistema suizo, ELO).
Son lógica con muchos casos borde (byes, números impares, desempates) que debe probarse a fondo.

## Decisión

Organizaremos `app/` en capas: `api` → `services` → `repositories` → `models`, más `schemas`
y `core`. Los algoritmos en `services/` serán **funciones puras** sin dependencias de FastAPI
ni de SQLAlchemy. Ver [vision-general](../arquitectura/vision-general.md).

## Alternativas consideradas

- **Todo en las rutas** — rápido al inicio, imposible de testear sin levantar HTTP y BD.
- **Arquitectura hexagonal completa** — más aislamiento, pero excesiva para el tamaño del proyecto.

## Consecuencias

- Tests unitarios rápidos y exhaustivos para los algoritmos (objetivo ≥95% de cobertura en `services/`).
- Un poco más de código de mapeo entre modelos ORM y estructuras de dominio.
