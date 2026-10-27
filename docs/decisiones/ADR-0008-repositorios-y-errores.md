---
tags: [adr, arquitectura]
estado: aceptado
fecha: 2026-10-27
---

# ADR-0008 Repositorios, transacciones y errores de aplicación

## Contexto

Con el primer CRUD (jugadores) hay que decidir dónde viven las consultas, quién confirma
las transacciones (`commit`) y cómo se convierten los errores (no existe, duplicado) en respuestas HTTP
sin que las capas internas conozcan HTTP.

## Decisión

- **Repositorios** (`app/repositories/`): una clase por agregado con las consultas. Reciben la sesión
  por inyección de dependencias (`PlayerRepositoryDep`). Hacen `flush`, **nunca `commit`**.
- **La ruta decide el `commit`**, una vez por petición, cuando todas las operaciones salieron bien.
  Así varias operaciones de distintos repositorios pueden formar una sola transacción.
- **Errores de aplicación** (`app/core/exceptions.py`): `NotFoundError`, `ConflictError`, sin relación
  con HTTP. Un manejador global (`app/api/errors.py`) los traduce a 404 / 409 con el formato estándar
  de FastAPI `{"detail": "..."}`.
- La unicidad (nombre de jugador) la garantiza **la base de datos** (`UNIQUE`); el repositorio traduce
  el `IntegrityError` a `ConflictError`. No se consulta antes "¿existe ya?", porque entre la consulta
  y el insert otra petición podría crear el mismo nombre.
- Los endpoints de recursos se publican bajo **`/api/v1`** desde ya (adelantado de la Fase 4) para no
  romper clientes después. `/health` queda en la raíz.

## Alternativas consideradas

- **Consultas directamente en las rutas** — menos archivos, pero rutas largas, consultas repetidas y
  difíciles de reutilizar desde la lógica de torneos.
- **Commit automático en la dependencia `get_session`** — menos código en cada ruta, pero el commit
  ocurriría después de construir la respuesta y un fallo del commit podría no reflejarse en ella.
- **Lanzar `HTTPException` desde el repositorio** — simple, pero acopla la capa de datos a HTTP.
- **Capa de servicios de aplicación para el CRUD** — útil cuando haya reglas (Fase 2); para CRUD
  simple solo añadiría código de paso.

## Consecuencias

- Cada ruta que escribe debe acordarse de `await session.commit()`; los tests de integración lo detectan
  (el dato no aparece en la siguiente petición).
- Tras un `rollback`, los objetos ORM expiran: no se deben leer sus atributos (ver el bug corregido en
  `PlayerRepository.save`).
- Al llegar la Fase 2 se introducirán servicios de aplicación para orquestar repositorios y algoritmos.
