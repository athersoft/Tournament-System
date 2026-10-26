---
name: adr
description: Crea un nuevo Architecture Decision Record en docs/decisiones/ cuando se elige entre alternativas técnicas reales (base de datos, librería, patrón, formato de API). Úsalo también si una decisión reemplaza a un ADR existente.
---

# Crear un ADR

Argumento opcional: título corto de la decisión.

1. Lista `docs/decisiones/` y toma el siguiente número (`ADR-NNNN`, 4 dígitos).
2. Si la decisión contradice o reemplaza un ADR aceptado, léelo primero.
3. Crea `docs/decisiones/ADR-NNNN-<slug-en-minusculas>.md` siguiendo la estructura de
   `docs/plantillas/adr.md` (las variables `{{date}}`/`{{title}}` son de Obsidian: sustitúyelas).
   - `estado: propuesto` salvo que la persona ya haya confirmado la decisión → `aceptado`.
   - **Alternativas consideradas**: al menos dos, con pros y contras honestos.
   - **Consecuencias**: incluye lo negativo y lo que queda pendiente.
4. Si reemplaza a otro ADR: en el antiguo cambia `estado: reemplazado` y añade
   "Reemplazado por [ADR-NNNN](ADR-NNNN-....md)". No modifiques el resto de su contenido.
5. Añade la fila al índice `docs/decisiones/README.md`.
6. Si afecta la arquitectura, enlaza el ADR desde `docs/arquitectura/vision-general.md`.

Enlaces siempre markdown relativos, nunca `[[wikilinks]]`. Redacción en español, concisa.
