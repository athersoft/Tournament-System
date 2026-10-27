---
name: cerrar-sesion
description: Cierra una sesión de trabajo actualizando la bitácora del día, el roadmap y el CHANGELOG en el vault de Obsidian.
disable-model-invocation: true
---

# Cerrar sesión de trabajo

Objetivo: que la próxima sesión (humana o de IA) pueda continuar sin depender de este chat.

1. Revisa qué cambió: `git status`, `git diff` y `git log` de la rama actual frente a `main`.
2. **Bitácora** — `docs/bitacora/YYYY-MM-DD.md` con la fecha de hoy:
   - Si no existe, créala con la estructura de `docs/plantillas/bitacora.md`.
   - Si existe, añade a sus secciones sin borrar lo anterior.
   - "Hecho": hechos concretos, no intenciones. "Pendiente": tareas accionables con `- [ ]`.
   - Menciona problemas encontrados y cómo se resolvieron (o que siguen abiertos).
3. **Roadmap** — `docs/roadmap/roadmap.md`: marca `[x]` solo lo que está realmente terminado
   (tests y CI pasando), añade tareas nuevas descubiertas y actualiza `actualizado:` y `fase_actual:`.
4. **CHANGELOG** — si hubo cambios visibles para el usuario, añádelos bajo `## [Unreleased]`
   (Added / Changed / Fixed / Removed).
5. Si se tomó una decisión técnica sin ADR, sugiere crearlo con `/adr`.
6. **Aprendizaje** — si la sesión introdujo conceptos nuevos que aún no tienen nota en
   `docs/aprendizaje/`, escríbela (problema → cómo funciona → dónde está en el código →
   errores típicos → ejercicios) y enlázala en `docs/aprendizaje/README.md`.
7. Muestra un resumen de lo actualizado. No hagas commit.
