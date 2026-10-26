---
tags: [adr, ia]
estado: aceptado
fecha: 2026-10-26
---

# ADR-0006 Desarrollo asistido por IA con contexto versionado

## Contexto

El proyecto se desarrolla con ayuda de asistentes de IA (Claude Code). Sin reglas explícitas,
la IA puede ignorar convenciones, repetir decisiones ya descartadas o introducir código que nadie
revisó. Además, el contexto de cada sesión se pierde al cerrarla.

## Decisión

- El contexto que necesita la IA vive **en el repositorio**: `CLAUDE.md` (reglas y comandos),
  `.claude/` (permisos y skills compartidos) y este vault (decisiones, roadmap, bitácora).
- Todo cambio generado con IA pasa por el mismo proceso que cualquier otro: rama, tests, CI y PR
  revisado por una persona.
- Los commits con aporte de IA se atribuyen con el trailer `Co-Authored-By`.
- Política completa: [Uso de IA](../ia/uso-de-ia.md).

## Alternativas consideradas

- **Uso ad-hoc sin reglas** — rápido, pero inconsistente y sin trazabilidad.
- **No usar IA** — renuncia a una herramienta productiva y a mostrar un flujo moderno de trabajo.

## Consecuencias

- `CLAUDE.md` y el vault deben mantenerse al día; una regla desactualizada es peor que ninguna.
- Transparencia ante revisores sobre qué se hizo con IA y cómo se verificó.
