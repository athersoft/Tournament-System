---
tags: [adr]
estado: aceptado
fecha: 2026-10-26
---

# ADR-0001 Registrar decisiones con ADRs

## Contexto

Las decisiones técnicas se pierden en conversaciones (incluidas las sesiones con asistentes de IA)
y en mensajes de commit. Sin un registro, es difícil justificar el diseño ante un revisor o
evitar que una sesión futura deshaga una decisión deliberada.

## Decisión

Documentaremos cada decisión técnica relevante como un ADR en `docs/decisiones/`,
numerado secuencialmente, usando la plantilla del vault.

## Alternativas consideradas

- **Solo commits/PRs** — sin costo extra, pero el "por qué" queda disperso y difícil de encontrar.
- **Wiki de GitHub** — vive fuera del repositorio, no se versiona junto al código.

## Consecuencias

- Cada PR que introduce una decisión de arquitectura incluye su ADR.
- Los asistentes de IA consultan este registro antes de proponer cambios estructurales.
