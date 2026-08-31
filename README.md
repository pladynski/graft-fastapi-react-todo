# Todo List App (Graftcode)

This is the original FastAPI + React todo app after a **migration by deletion**. We did not rewrite the backend.

We deleted REST: FastAPI `main.py` routes, OpenAPI, `HTTPException` translation, and the JavaScript HTTP client. The existing `TodoController` methods are now the graft contract. Business logic in `services.py` is unchanged — the controller still calls `TodoService` the same way it did when those methods were HTTP handlers. `gg` hosts the controller; that is the only public API.

## Quick start (Docker)

```bash
docker compose up --build
```

| Service | URL | What it is |
| --- | --- | --- |
| Frontend | http://localhost:5173 | React app |
| Gateway (WS + Vision routes) | http://localhost:8000 | `gg` on `--port 8000` |
| Vision | http://localhost:8000 | Graftcode Vision UI |
| Install command | http://localhost:8000/npm | exact `npm install --registry …` |
| Contract (UGM) | http://localhost:8000/libraries | machine-readable methods/types |

Wait until `curl -sS http://localhost:8000/npm` returns HTTP 200. That body is the **current** graft install command. The registry GUID rotates on every Gateway restart unless you pass a real `--projectKey` from [portal.graftcode.com](https://portal.graftcode.com). Never invent a placeholder key — `gg` fails with `JwtToken decode failed`. The Gateway needs outbound HTTPS to `grft.dev` so it can publish that graft; compose uses the default Docker bridge for that.

The frontend container entrypoint polls `/npm`, runs that exact install command, then starts Vite. In the browser the graft is configured with:

```js
GraftConfig.host = import.meta.env.VITE_GRAFT_HOST ?? "ws://localhost:8000/ws";
GraftConfig.stateless = true;
```

`VITE_GRAFT_HOST` defaults to `ws://localhost:8000/ws` (the compose-mapped Gateway WebSocket). Copy host/path from Vision / Gateway output if you change ports.

## Local frontend (Gateway already in Docker)

```bash
# terminal 1 — Gateway only
docker compose up --build backend

# terminal 2 — install the CURRENT graft, then run Vite
cd frontend
npm install
npm run install:graft    # curls http://localhost:8000/npm and runs that command
npm run dev
```

Do not hand-write `fetch` / axios clients. After a Gateway restart without a project key, run `npm run install:graft` again so you pick up the new GUID.

## Public contract

`backend/controllers.py` — `TodoController` static methods, same names as the old HTTP controller:

- `get_all_todos() -> list[TodoResponse]`
- `get_todo(todo_id: int) -> TodoResponse`
- `create_todo(title: str, description: str) -> TodoResponse`
- `update_todo(todo_id: int, title: str, description: str) -> TodoResponse`
- `toggle_todo_completion(todo_id: int) -> TodoResponse`
- `delete_todo(todo_id: int) -> str`

`create_todo` / `update_todo` take primitive fields instead of FastAPI body models. `delete_todo` returns the service message string (`dict` is not a portable graft type). `TodoNotFoundException` is no longer mapped to HTTP 404 — the message propagates as a plain exception.

Layers that stayed: `services.py` (`TodoService`), `repositories.py`, `models.py`, `schemas.py`.

## Tests

```bash
# backend unit tests (call TodoController, which delegates to TodoService)
cd backend && APP_ENV=test python3 -m pytest test_todo_controller.py -v

# consumer smoke against a running Gateway (create + list + toggle + delete)
cd frontend && npm run smoke

# Playwright against docker compose (stack must already be up)
cd e2e && python3 -m pytest test_todo_e2e.py -v
```

## Project layout

```
backend/controllers.py  # graft facade; delegates to TodoService
backend/services.py      # unchanged business logic
backend/repositories.py
backend/models.py
backend/schemas.py
backend/Dockerfile       # gg --modules ./controller/ (facade + schemas only)
frontend/src/graft/       # GraftConfig.host + generated controller import
frontend/scripts/         # install-graft.sh, smoke.mjs, clear-todos.mjs
.cursor/rules/            # official Graftcode Cursor rules
```
