---
tags: [aprendizaje, python, async]
fecha: 2026-10-27
---

# 01 · async / await

## El problema

Un restaurante con **un solo mesero**:

- **Mesero síncrono**: toma el pedido de la mesa 1, lo lleva a cocina y **se queda parado esperando**.
  Las mesas 2, 3 y 4 no son atendidas.
- **Mesero asíncrono**: deja el pedido en cocina y **mientras se cocina** atiende la mesa 2, luego la 3.
  Cuando un plato está listo, lo lleva.

La cocina no es más rápida: el mesero **no pierde tiempo esperando**. En una API, "la cocina" es la
base de datos, otra API o el disco. El servidor pasa la mayor parte del tiempo esperando; aprovechar
esas esperas permite atender muchas peticiones a la vez con un solo proceso.

## Cómo funciona

- `async def` declara una función que **puede pausarse** (una *corrutina*).
- `await` significa "aquí voy a esperar algo; mientras tanto, atiende otra cosa".
- El **event loop** es el mesero: decide qué corrutina continúa cuando otra está esperando.

Pruébalo: guarda esto como `prueba_async.py` fuera del proyecto y ejecútalo con `python prueba_async.py`.

```python
import asyncio
import time


async def pedir_plato(mesa: int) -> str:
    print(f"Mesa {mesa}: pedido enviado a la cocina")
    await asyncio.sleep(2)  # simula esperar a la base de datos
    return f"Mesa {mesa}: plato servido"


async def main() -> None:
    inicio = time.perf_counter()
    resultados = await asyncio.gather(pedir_plato(1), pedir_plato(2), pedir_plato(3))
    print(resultados)
    print(f"Tiempo total: {time.perf_counter() - inicio:.1f} s")


asyncio.run(main())
```

Tarda **~2 segundos, no 6**: las tres esperas ocurren a la vez.

## En el proyecto

```python
# app/api/routes/health.py
async def health(settings: SettingsDep, session: SessionDep, response: Response) -> HealthResponse:
    database_ok = await is_database_available(session)
```

```python
# app/core/database.py
async def is_database_available(session: AsyncSession) -> bool:
    await session.execute(text("SELECT 1"))  # ← aquí el servidor atiende otras peticiones
```

Toda la cadena es async: FastAPI → `AsyncSession` → driver `asyncpg`. Por eso el
[ADR-0007](../decisiones/ADR-0007-postgresql-sqlalchemy.md) eligió `asyncpg`.

## Errores típicos

**1. Olvidar el `await`**

```python
resultado = session.execute(...)  # ❌ no ejecuta nada: devuelve una corrutina "dormida"
resultado = await session.execute(...)  # ✅
```

Python avisa con `RuntimeWarning: coroutine ... was never awaited`; mypy strict también lo detecta
en muchos casos.

**2. Bloquear el event loop**

```python
async def mala_ruta():
    time.sleep(2)  # ❌ el mesero se duerme: TODO el servidor se detiene
    requests.get("...")  # ❌ requests no es async


async def buena_ruta():
    await asyncio.sleep(2)  # ✅
    await httpx.AsyncClient().get("...")  # ✅
```

Dentro de `async def`, solo operaciones "awaiteables". Una llamada bloqueante frena a todos los usuarios.

**3. `await` fuera de `async def`**

Es un error de sintaxis. Para arrancar código async desde código normal se usa `asyncio.run(...)`,
como hace [alembic/env.py](../../alembic/env.py).

## Reglas prácticas

- FastAPI acepta `def` y `async def`. Con `def`, ejecuta la ruta en un hilo aparte para no bloquear.
  Regla: si usas `await` dentro → `async def`; si usas una librería bloqueante → `def`.
- **async no acelera el cálculo** (por ejemplo, el algoritmo del sistema suizo). Solo aprovecha las
  esperas. Por eso los servicios de dominio de la Fase 2 serán funciones normales (`def`).

## Ejercicios

1. Ejecuta `prueba_async.py`. Luego cambia `await asyncio.sleep(2)` por `time.sleep(2)` (y quita
   el `await`). ¿Cuánto tarda ahora? ¿Por qué?
2. Quita el `await` de `asyncio.gather(...)` y lee el error.
3. En [database.py](../../app/core/database.py), quita el `await` de `session.execute(...)` y corre
   `mypy` y `pytest`. ¿Quién detecta el error primero?
