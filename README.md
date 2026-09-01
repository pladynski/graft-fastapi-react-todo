# Todo List App — Graftcode migration

Any existing GitHub project can switch to Graftcode in a tiny, obvious diff: **less code, more readable for AI, integration layer gone.**

This fork of [makevoid/vite-python-fastapi-todolist](https://github.com/makevoid/vite-python-fastapi-todolist) shows that on the original files.

## Before → after

1. **Delete FastAPI.** `backend/main.py` (routes, OpenAPI) is gone. The image runs `./gg` (installer unpacks the binary into WORKDIR) to host `TodoController`.
2. **Strip HTTP from the controller.** Same methods (`get_all_todos`, `create_todo`, …) still call `TodoService`. No FastAPI, no `HTTPException`.
3. **Dataclass the public schemas.** `TodoResponse` / `TodoCreate` / `TodoUpdate` stay in `schemas.py` — `BaseModel` → `@dataclass`.
4. **Swap HTTP for a graft inside `TodoService.js`.** Same class, same methods (`fetchTodos`, `createTodo`, …). `ApiService.js` is gone. `useTodos` is unchanged.

## Run

```bash
docker compose up --build
```

Wait until `curl -sS http://localhost:8000/npm` is 200. That body is the exact `npm install --registry …` command (GUID rotates unless you pass a real `--projectKey` from [portal.graftcode.com](https://portal.graftcode.com) — never invent one).

| | |
| --- | --- |
| App | http://localhost:5173 |
| Gateway / Vision | http://localhost:8000 |
| Install command | http://localhost:8000/npm |

Local frontend against a running Gateway:

```bash
cd frontend
npm install
npm run install:graft   # copies the command from /npm
npm run dev
```

AI assistant rules are not in this repo, so the migration diff stays small. Install them from the project root:

```powershell
iwr grft.dev/get | iex
```

```bash
curl -fsSL grft.dev/get | sh
```
