---
tags: [adr]
estado: aceptado
fecha: 2026-10-26
---

# ADR-0002 FastAPI + Pydantic v2 como framework

## Contexto

Se necesita una API REST en Python, con validación de datos, documentación automática
y soporte asíncrono para la base de datos.

## Decisión

Usaremos **FastAPI** con **Pydantic v2** para validación/serialización y **pydantic-settings**
para la configuración por variables de entorno.

## Alternativas consideradas

- **Django + DRF** — muy completo, pero más pesado y opinado de lo necesario para una API pura.
- **Flask** — minimalista, pero requiere ensamblar validación, OpenAPI y async a mano.

## Consecuencias

- OpenAPI/Swagger en `/docs` sin trabajo extra.
- Tipado de punta a punta, verificable con mypy (`pydantic.mypy` plugin).
- La aplicación se construye con una *app factory* (`create_app()`) para aislar los tests.
