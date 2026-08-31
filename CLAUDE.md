# CLAUDE.md

This file provides guidance when working with code in this repository.

## Project Overview

Full-stack todo app: React/Vite frontend + the original layered Python backend hosted by Graftcode Gateway (`gg`) in Docker. `TodoController` static methods are the public contract. They delegate to the existing `TodoService`. Do not add FastAPI routes, REST handlers, or hand-written fetch clients.

## Development Commands

### Docker (default)

```bash
docker compose up --build
```

Gateway listens on host port 8000 (WS + Vision `/npm` `/libraries`). Frontend is on 5173. The frontend entrypoint waits for `http://backend:8000/npm` and runs the exact printed `npm install --registry …` command before Vite starts.

### Backend unit tests

```bash
cd backend
APP_ENV=test python3 -m pytest test_todo_controller.py -v
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

### Backend (existing layers + thin graft facade)

- `backend/controllers.py`: public `TodoController` static methods (no FastAPI / no `HTTPException`)
- `backend/services.py`: original `TodoService` business logic — unchanged
- `backend/repositories.py`, `models.py`, `schemas.py`: original data / schema layers
- Hosted with `gg --modules ./controller/ --port 8000 --corsAllowedOrigins *`
- `--modules` contains only the facade + `schemas.py` so GMA does not scan peewee models

### Frontend

- Installs the generated graft from the live Gateway `/npm` command
- `frontend/src/graft/config.js` sets `GraftConfig.host` and `GraftConfig.stateless = true`
- `useTodos` calls `TodoController` methods; no REST `ApiService`

## Graftcode rules

Follow `.cursor/rules/` (especially `graftcode-router`, `graftcode-python`, `graftcode-typescript-node-nextjs`). They override REST instincts.
