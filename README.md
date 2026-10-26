# Sistema de Torneos

API REST para la gestión de torneos competitivos: eliminación directa, sistema suizo y ranking ELO.

> 🚧 En desarrollo — fase 0 (fundaciones del repositorio).

## Stack

- **Python 3.11+** · **FastAPI** · **Pydantic v2**
- Calidad: **Ruff**, **mypy** (strict), **pytest**, **pre-commit**
- CI: **GitHub Actions**

## Puesta en marcha

```bash
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

# 5. Levantar el servidor
uvicorn app.main:app --reload
```

La documentación interactiva queda disponible en <http://localhost:8000/docs>.

## Comandos útiles

| Comando | Descripción |
|---|---|
| `pytest` | Ejecuta los tests |
| `pytest --cov` | Tests con reporte de cobertura |
| `ruff check .` | Lint |
| `ruff format .` | Formatea el código |
| `mypy` | Chequeo de tipos |
| `pre-commit run --all-files` | Ejecuta todos los hooks |

## Estructura

```
app/
├── api/          # Rutas y dependencias de FastAPI
├── core/         # Configuración y base de datos
├── models/       # Modelos ORM
├── schemas/      # Schemas Pydantic (entrada/salida)
└── services/     # Lógica de dominio (brackets, suizo, ELO)
tests/
├── unit/
└── integration/
```

## Flujo de trabajo

- `main` siempre está estable; cada cambio entra mediante Pull Request.
- Ramas: `feat/...`, `fix/...`, `chore/...`, `docs/...`.
- Commits según [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/).

## Licencia

[MIT](LICENSE)
