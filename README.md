# Todo List App (Graftcode)

A React + Vite frontend that calls a Python todo module through a Graft. The public Python methods are the contract. Graftcode Gateway (`gg`) hosts the module in Docker — there is no FastAPI / REST / OpenAPI surface.

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

Wait until `curl -sS http://localhost:8000/npm` returns HTTP 200. That body is the **current** graft install command. The registry GUID rotates on every Gateway restart unless you pass a real `--projectKey` from [portal.graftcode.com](https://portal.graftcode.com). Never invent a placeholder key — `gg` fails with `JwtToken decode failed`.

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

`backend/todoservice/todo_service.py` — `TodoService` static methods:

- `list_todos() -> list[str]` — flat snapshots: `id, title, description, completed` repeated
- `get_todo(todo_id: str) -> list[str]` — `[id, title, description, completed]`
- `create_todo(title: str, description: str) -> list[str]`
- `update_todo(todo_id: str, title: str, description: str) -> list[str]`
- `toggle_todo(todo_id: str) -> list[str]`
- `delete_todo(todo_id: str) -> bool`

Ids are strings. `completed` is `"true"` or `"false"`. Collections are plain string arrays so every consumer language gets primitives (not opaque remote objects).

## Tests

```bash
# backend unit tests (call TodoService directly, isolated sqlite files)
cd backend && python3 -m pytest test_todo_service.py -v

# consumer smoke against a running Gateway (create + list + toggle + delete)
cd frontend && npm run smoke

# Playwright against docker compose (stack must already be up)
cd e2e && python3 -m pytest test_todo_e2e.py -v
```

## Project layout

```
backend/todoservice/     # the only module passed to gg --modules
backend/Dockerfile       # installs gg.deb (arch-detected) and runs gg
frontend/src/graft/       # GraftConfig.host + TodoService imports
frontend/scripts/         # install-graft.sh, smoke.mjs, clear-todos.mjs
.cursor/rules/            # official Graftcode Cursor rules
```
