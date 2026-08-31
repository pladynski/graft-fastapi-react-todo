# CLAUDE.md

This file provides guidance when working with code in this repository.

## Project Overview

Full-stack todo app: React/Vite frontend + a plain Python Graftcode module hosted by Graftcode Gateway (`gg`) in Docker. Public methods on `TodoService` are the contract. Do not add FastAPI controllers, REST routes, or hand-written fetch clients.

## Development Commands

### Docker (default)

```bash
docker compose up --build
```

Gateway listens on host port 8000 (WS + Vision `/npm` `/libraries`). Frontend is on 5173. The frontend entrypoint waits for `http://backend:8000/npm` and runs the exact printed `npm install --registry …` command before Vite starts.

### Backend unit tests

```bash
cd backend
python3 -m pytest test_todo_service.py -v
```

### Frontend (Gateway already running)

```bash
cd frontend
npm install
npm run install:graft
npm run dev
npm run smoke
```

GUID on `/npm` rotates when Gateway restarts without a real `--projectKey`. Never pass a fake project key.

## Architecture

### Backend (Graftcode Python module)

- `backend/todoservice/todo_service.py`: public `TodoService` static methods
- Persistence is sqlite3, kept off the public surface
- Hosted with `gg --modules ./todoservice/ --port 8000 --corsAllowedOrigins *`
- Ids are strings; todo snapshots are `list[str]` (`id, title, description, completed`)

### Frontend

- Installs `@graft/pypi-todo-service` from the live Gateway `/npm` command
- `frontend/src/graft/config.js` sets `GraftConfig.host` and `GraftConfig.stateless = true`
- `useTodos` calls `TodoService` methods; no REST `ApiService`

## Graftcode rules

Follow `.cursor/rules/` (especially `graftcode-router`, `graftcode-python`, `graftcode-typescript-node-nextjs`). They override REST instincts.
