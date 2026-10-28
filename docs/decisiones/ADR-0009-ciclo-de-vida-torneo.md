---
tags: [adr, dominio]
estado: aceptado
fecha: 2026-10-27
---

# ADR-0009 Ciclo de vida del torneo como reglas puras y acciones explícitas

## Contexto

Un torneo pasa por estados (`draft → registration → in_progress → finished`, o `cancelled`) y
cada estado permite operaciones distintas: solo se inscribe con inscripciones abiertas, el formato
solo cambia en borrador, etc. Hay que decidir dónde viven esas reglas, cómo se cambia de estado
desde la API y cómo se guardan los estados en la base.

## Decisión

- **Reglas en `app/services/tournament_lifecycle.py`** como funciones puras (`ensure_transition`,
  `ensure_registration_open`, `ensure_has_capacity`, …) que reciben estados y números y lanzan
  `ConflictError` (409). La tabla `ALLOWED_TRANSITIONS` es la única fuente de verdad del diagrama.
- **Acciones explícitas** para cambiar de estado: `POST /tournaments/{id}/open-registration`,
  `POST /tournaments/{id}/cancel` (y `start` en la Fase 2). El campo `status` no se acepta en
  `POST` ni en `PATCH`.
- **Enums como `VARCHAR` + `CHECK`** (`native_enum=False`), guardando los valores en minúscula
  (`"draft"`), definidos en `app/core/enums.py` como `StrEnum`.
- **`SELECT ... FOR UPDATE`** sobre el torneo en las operaciones que leen y luego deciden
  (inscribir con cupo, cambiar de estado, editar el cupo).

## Alternativas consideradas

- **`PATCH {"status": "cancelled"}`** — un solo endpoint, pero mezcla edición de datos con
  transiciones que tienen efectos (en la Fase 2, `start` genera las partidas) y complica validar.
- **Librería de máquinas de estado** (`transitions`, `python-statemachine`) — más funciones, pero una
  dependencia extra para una tabla de 5 filas.
- **Reglas dentro del modelo ORM** (`tournament.open_registration()`) — cómodo, pero acopla el dominio a
  SQLAlchemy y obliga a la base de datos para testear las reglas.
- **ENUM nativo de PostgreSQL** — más estricto y compacto, pero agregar un valor exige `ALTER TYPE`,
  que no se puede deshacer fácilmente en una migración.

## Consecuencias

- Las reglas se prueban con tests unitarios sin base de datos (51 tests en ~0,1 s).
- Agregar un estado = agregar el valor al `StrEnum` + una fila en `ALLOWED_TRANSITIONS` + una
  migración que actualice el `CHECK`.
- Las rutas orquestan (cargar → validar con reglas puras → guardar → commit), siguiendo
  [ADR-0008](ADR-0008-repositorios-y-errores.md). Si la orquestación crece en la Fase 2, se moverá a
  servicios de aplicación.
