---
tags: [adr, documentacion]
estado: aceptado
fecha: 2026-10-26
---

# ADR-0005 Documentación como vault de Obsidian en `docs/`

## Contexto

Se quiere usar Obsidian para tomar notas, planificar y documentar, sin que la documentación
quede fuera del repositorio ni deje de verse correctamente en GitHub.

## Decisión

La carpeta `docs/` es un vault de Obsidian versionado con el código. Se configura para usar
**enlaces markdown relativos** (no wikilinks) y diagramas Mermaid. Solo se versiona la
configuración compartida de `.obsidian/` (`app.json`, `templates.json`); el estado local del
editor (`workspace*.json`, caché, papelera) se ignora en git.

## Alternativas consideradas

- **Vault separado fuera del repo** — notas privadas, pero desconectadas del código y del historial.
- **Wikilinks `[[nota]]`** — más cómodos en Obsidian, pero se rompen al leer en GitHub.

## Consecuencias

- La documentación se revisa en los mismos PR que el código.
- Los asistentes de IA pueden leer el vault como contexto del proyecto.
- Las notas personales que no deban publicarse deben vivir fuera de `docs/`.
