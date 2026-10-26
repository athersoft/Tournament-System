---
tags: [inicio]
---

# Documentación — Sistema de Torneos

Esta carpeta es un **vault de Obsidian** y también se lee directamente en GitHub.
Es la memoria del proyecto: lo que se decidió, por qué, y en qué punto estamos.

## Mapa

| Sección | Para qué sirve |
|---|---|
| [Arquitectura](arquitectura/vision-general.md) | Capas, reglas de dependencia y flujo de una petición |
| [Glosario](arquitectura/glosario.md) | Vocabulario del dominio (bye, Buchholz, ELO, …) |
| [Decisiones (ADR)](decisiones/README.md) | Registro de decisiones técnicas y sus motivos |
| [Roadmap](roadmap/roadmap.md) | Fases, milestones y estado actual |
| [Bitácora](bitacora/) | Notas por sesión de trabajo |
| [Uso de IA](ia/uso-de-ia.md) | Política y flujo de trabajo con asistentes de IA |

## Convenciones del vault

- **Enlaces markdown relativos** (`[texto](ruta.md)`), no `[[wikilinks]]`, para que funcionen en GitHub.
  Ya está configurado en `.obsidian/app.json`.
- **Frontmatter** en cada nota (`tags`, `estado`, `fecha`) para poder filtrar.
- **Plantillas** en [`plantillas/`](plantillas/) — en Obsidian: *Insertar plantilla* (`Ctrl+P` → "Templates").
- **Diagramas** con Mermaid (se renderizan en Obsidian y en GitHub).
- Imágenes y adjuntos en `assets/`.
