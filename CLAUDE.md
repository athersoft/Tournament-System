# CLAUDE.md

API REST de gestión de torneos (eliminación directa, sistema suizo, ELO) con FastAPI.
Proyecto de portafolio: la calidad del proceso importa tanto como el código.

## Antes de empezar una tarea

1. Lee `docs/roadmap/roadmap.md` (fase actual) y la nota más reciente de `docs/bitacora/`.
2. Si la tarea toca arquitectura, revisa `docs/decisiones/` — no contradigas un ADR aceptado
   sin proponer uno nuevo que lo reemplace.
3. Usa el vocabulario de `docs/arquitectura/glosario.md` en nombres de código.
4. Para cambios de más de un archivo, propone un plan breve antes de editar.

## Comandos

Entorno virtual en `.venv` (Windows: `.venv\Scripts\`). Instalar: `pip install -e ".[dev]"`.

```bash
pytest                       # tests
pytest --cov                 # tests + cobertura (mínimo 80%)
ruff check . --fix           # lint
ruff format .                # formato
mypy                         # tipos (strict)
pre-commit run --all-files   # todo lo anterior + hooks
uvicorn app.main:app --reload
```

Una tarea no está terminada hasta que `pre-commit run --all-files` y `pytest --cov` pasan.

## Arquitectura

Detalle en `docs/arquitectura/vision-general.md`. Reglas que no se rompen:

- `app/services/` contiene lógica de dominio **pura**: no importa `fastapi` ni `sqlalchemy`.
- `app/schemas/` (Pydantic, API) y `app/models/` (ORM) están separados; no reutilizar uno como otro.
- Las rutas no contienen lógica de negocio: validan, delegan en servicios y mapean errores HTTP.
- Configuración solo vía `app.core.config.get_settings()`; nunca leer `os.environ` directo.
- La app se crea con `create_app()`; los tests usan el fixture `client` de `tests/conftest.py`.

## Convenciones de código

- Código, identificadores y docstrings en **inglés**; documentación y mensajes de usuario en **español**.
- Tipado completo (mypy strict). `Annotated[..., Depends(...)]` para dependencias de FastAPI.
- Tests: `tests/unit/` para servicios puros, `tests/integration/` para endpoints.
  Nombre: `test_<comportamiento>_<condición>`. Cubrir casos borde (byes, números impares, empates).
- No añadir dependencias sin preguntar; si se aprueban, van en `pyproject.toml`.

## Git

- Nunca commitear en `main`: rama `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`, `test/`.
- Conventional Commits: `feat(swiss): add buchholz tiebreak`.
- No hacer commit ni push salvo que se pida explícitamente.
- Actualizar `CHANGELOG.md` (sección `Unreleased`) en cambios visibles para el usuario.

## Documentación (vault de Obsidian en `docs/`)

- Enlaces markdown relativos `[texto](ruta.md)`, nunca `[[wikilinks]]`.
- Toda nota lleva frontmatter (`tags`, y `fecha`/`estado` cuando aplique).
- Decisión técnica con alternativas reales → nuevo ADR (skill `/adr`).
- Al cerrar una sesión de trabajo → skill `/cerrar-sesion`.

## Seguridad

- No leer ni mostrar `.env`. Los valores de ejemplo van en `.env.example`.
- Sin secretos en código, tests ni documentación.
