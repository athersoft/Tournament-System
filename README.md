# Sistema de Torneos

API REST para la gestión de torneos competitivos: eliminación directa, sistema suizo y ranking ELO.

> 🚧 En desarrollo — fase 1 (núcleo de datos).

## Stack

- **Python 3.11+** · **FastAPI** · **Pydantic v2**
- **PostgreSQL 17** · **SQLAlchemy 2** (async) · **Alembic**
- Calidad: **Ruff**, **mypy** (strict), **pytest**, **pre-commit**
- CI: **GitHub Actions**

## Puesta en marcha

Requisitos: Python 3.11+ y [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
# 0. Levantar PostgreSQL (crea las bases torneos y torneos_test)
docker compose up -d
# 1. Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\Activate.ps1       # Windows PowerShell

# 2. Instalar dependencias (incluye herramientas de desarrollo)
pip install -e ".[dev]"

# 3. Configurar variables de entorno
cp .env.example .env

# 4. Instalar hooks de git
pre-commit install

# 5. Aplicar migraciones
alembic upgrade head

# 6. Levantar el servidor
uvicorn app.main:app --reload
```

La documentación interactiva queda disponible en <http://localhost:8000/docs>.

## Comandos útiles

| Comando | Descripción |
|---|---|
| `docker compose up -d` / `down` | Levanta / detiene PostgreSQL |
| `alembic upgrade head` | Aplica las migraciones pendientes |
| `alembic revision --autogenerate -m "..."` | Genera una migración desde los modelos |
| `pytest` | Ejecuta los tests (requiere PostgreSQL arriba) |
| `pytest --cov` | Tests con reporte de cobertura |
| `ruff check .` | Lint |
| `ruff format .` | Formatea el código |
| `mypy` | Chequeo de tipos |
| `pre-commit run --all-files` | Ejecuta todos los hooks |

## Estructura

```
app/
├── api/          # Rutas, dependencias y traducción de errores a HTTP
├── core/         # Configuración, base de datos, constantes y errores
├── models/       # Modelos ORM
├── repositories/ # Consultas a la base de datos
├── schemas/      # Schemas Pydantic (entrada/salida)
└── services/     # Lógica de dominio (brackets, suizo, ELO)
tests/
├── unit/
└── integration/
```

## API

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/health` | Estado del servicio y de la base de datos |
| `POST` | `/api/v1/players` | Crear jugador |
| `GET` | `/api/v1/players?limit=&offset=&search=` | Listar jugadores (paginado) |
| `GET` | `/api/v1/players/{id}` | Ver jugador |
| `PATCH` | `/api/v1/players/{id}` | Renombrar jugador |
| `DELETE` | `/api/v1/players/{id}` | Eliminar jugador (409 si está inscrito) |
| `POST` | `/api/v1/tournaments` | Crear torneo (nace como borrador) |
| `GET` | `/api/v1/tournaments?status=&format=` | Listar torneos (paginado, con filtros) |
| `GET` / `PATCH` / `DELETE` | `/api/v1/tournaments/{id}` | Ver, editar o eliminar torneo |
| `POST` | `/api/v1/tournaments/{id}/open-registration` | Abrir inscripciones |
| `POST` | `/api/v1/tournaments/{id}/cancel` | Cancelar torneo |
| `POST` / `GET` | `/api/v1/tournaments/{id}/registrations` | Inscribir jugador / listar inscritos |
| `DELETE` | `/api/v1/tournaments/{id}/registrations/{player_id}` | Desinscribir jugador |

Documentación interactiva completa en `/docs`.

## Documentación

La carpeta [`docs/`](docs/README.md) es un vault de [Obsidian](https://obsidian.md) versionado con el código
(ábrela con *Open folder as vault*). Incluye:

- [Arquitectura](docs/arquitectura/vision-general.md) y [glosario del dominio](docs/arquitectura/glosario.md)
- [Registro de decisiones (ADR)](docs/decisiones/README.md)
- [Roadmap](docs/roadmap/roadmap.md) y bitácora de desarrollo

## Desarrollo asistido por IA

El proyecto se desarrolla con [Claude Code](https://claude.com/claude-code) bajo una
[política explícita](docs/ia/uso-de-ia.md): el contexto vive en el repo ([`CLAUDE.md`](CLAUDE.md),
`.claude/`, ADRs), todo cambio pasa por tests, CI y revisión humana, y los commits con aporte
de IA se atribuyen con `Co-Authored-By`.

## Flujo de trabajo

- `main` siempre está estable; cada cambio entra mediante Pull Request.
- Ramas: `feat/...`, `fix/...`, `chore/...`, `docs/...`.
- Commits según [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/).

## Licencia

[MIT](LICENSE)
