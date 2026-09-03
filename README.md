# 📝 Todo List App

<div align="center">

![Tests](https://img.shields.io/badge/Tests-25%20Passing-success?style=for-the-badge)
<!-- insert other badges here -->

**A full-stack todo list app repo template to kickstart any of your projects**

*Built with Graftcode + React Vite, JSX + Comprehensive Integration Testing*

Iterate from a todo list to any app. Use this repo as a base.

</div>

This project was changed from the standard legacy FastAPI approach, which binds code to an integration method (REST), to grafting: you call remote methods as if they were local. To keep developing it with AI, install the Graftcode skill from the project root:

```powershell
iwr grft.dev/get | iex
```

```bash
curl -fsSL grft.dev/get | sh
```

## Why Graftcode (instead of FastAPI / REST)

This is a **real migration**, not a rewrite. `TodoService`, the repository, and Peewee models stayed. We deleted the integration method.

- **Delete:** FastAPI routes / CORS app, `ApiService.js`, HTTPException → status maps, TestClient URL asserts
- **Keep:** the same public methods and DTOs
- **Gain:** less code, transport decoupled, remote calls look local, MCP from Graftcode Vision, diffs AI can actually read

**Integration / transport plumbing** (this demo: `main.py`, `ApiService.js`, HTTP `TodoService.js`, FastAPI lines in `controllers.py`, HTTP asserts in `test_api.py`):

- **Before:** ~290 lines
- **After:** ~95 lines
- **Removed:** ~195 lines → **≈67% less** integration code

File sizes that drive that: `main.py` 85 → 20, `ApiService.js` 84 → 0 (deleted), `test_api.py` 227 → 179 (HTTP asserts ~48 → ~0). The PR as a whole is **+275 / −398** (net deletions).

**AI-assisted workflows:** fewer integration lines in context → higher context efficiency. Future AI PRs touch business methods, not HTTP glue — cleaner diffs, lower token use, because models aren’t rewriting controllers, clients, or status maps.

https://graftcode.com · https://github.com/grft-dev/graftcode · https://docs.graftcode.com

Try it: `docker compose up --build` — app on :5173, Graftcode Vision on :8000.

### Quick Start TLDR

- 1 - Clone the repo
- 2 - Run claude code or your favourite coding CLI
- 3 - Run this prompt: `this is a todolist app - you need to change this todolist app to be a .... `
- 4 - profit!

---

## 🏗️ Project Structure

### Backend Architecture (Python/Graftcode)

```
backend/
├── main.py              # DB bootstrap / --initMethod (old FastAPI lifespan startup)
├── models.py            # Database models using Peewee ORM
├── schemas.py           # Dataclass models for request/response validation
├── services.py          # Business logic layer with service classes
├── controllers.py       # Graftcode public surface (delegates to TodoService)
├── repositories.py      # Data access layer with repository pattern
└── requirements.txt     # Python dependencies
```

**Object-Oriented Design Patterns:**

- **Service Layer**: `TodoService` handles all business logic operations
- **Repository Pattern**: `TodoRepository` manages data access and response model conversion
- **Controller Layer**: `TodoController` public methods are the graft contract
- **Custom Exceptions**: Domain-specific exceptions for better error handling
- **Dependency Injection**: Clean separation of concerns with minimal coupling

### Frontend Architecture (React/Vite)

```
frontend/
├── src/
│   ├── App.jsx                    # Main application component
│   ├── main.jsx                   # Application entry point with providers
│   ├── services/
│   │   └── TodoService.js         # Todo operations via a graft (not HTTP)
│   ├── hooks/
│   │   └── useTodos.js            # Custom hook for todo operations
│   └── index.css                  # Global styles
├── package.json             # Dependencies and scripts
├── vite.config.js          # Build configuration
└── playwright.config.js    # E2E test configuration
```

### End-to-End Testing

```
e2e/
├── test_todo_e2e.py    # Comprehensive user workflow tests
└── pyproject.toml      # Test configuration
```

## 🚀 Quick Start

<div align="center">

### ⚡ **Get Running in 60 Seconds**

</div>

### Prerequisites
- **Python 3.11+** 🐍
- **Node.js 18+** 📦 
- **npm/yarn** ⚙️

### 1. Clone & Setup
```bash
git clone <repository-url>
cd vite-python-fastapi-todolist

# Backend setup 🐍
cd backend
pip install -r requirements.txt

# Frontend setup ⚛️
cd ../frontend
npm install
```

### 2. Development Mode
```bash
# Gateway (:8000) + frontend (:5173)
docker compose up --build
# wait until http://localhost:8000/npm is 200
```

Or locally, with the Gateway already running:

```bash
# Terminal 1: Gateway (Port 8000) 🚀
docker compose up --build backend

# Terminal 2: Frontend (Port 5173) ⚡
cd frontend
npm run install:graft    # exact command from http://localhost:8000/npm
npm run dev
```

### 3. Run Tests 🧪
```bash
# 🌐 End-to-end tests (13 tests, 10.4s)
cd e2e && python3 -m pytest test_todo_e2e.py -v

# ⚡ Quick smoke test
python3 -m pytest test_todo_e2e.py::TestTodoAppE2E::test_app_title -v
```

<div align="center">

### 🎉 **That's it! Your todo app is live!**

**Frontend**: http://localhost:5173 | **Gateway**: http://localhost:8000 | **Install command**: http://localhost:8000/npm

</div>

## 📡 API Reference

`TodoController` methods (hosted by `./gg`) are the contract — not REST routes.

| Method | Description |
|--------|-------------|
| `get_all_todos()` | Get all todos |
| `create_todo(todo)` | Create new todo |
| `get_todo(todo_id)` | Get specific todo |
| `update_todo(todo_id, update)` | Update todo |
| `toggle_todo_completion(todo_id)` | Toggle todo completion |
| `delete_todo(todo_id)` | Delete todo |

Frontend `TodoService.js` calls these via a graft (`npm run install:graft` copies the command from `http://localhost:8000/npm`).

### Example

**Create Todo**
```js
todoService.createTodo("Learn Graftcode", "Build a todo app with Python and React")
```

**Toggle Todo Completion**
```js
todoService.toggleTodoCompletion(id)
```

## 🔧 Development Workflow

### Day-to-Day Development
1. **Start Services**: Gateway (port 8000) + Frontend (port 5173). Wait until `/npm` is 200.
2. **Graft install command**: http://localhost:8000/npm (copy that exact `npm install`)
3. **Hot Reload**: Frontend Vite supports hot reload for rapid development
4. **Testing**: Run E2E tests for integration validation

### Key Development URLs
- **Frontend**: http://localhost:5173
- **Backend API**: ws://localhost:8000/ws
- **API Documentation**: http://localhost:8000 **(Graftcode Vision)**

---

NOTE:

Integration tests passing in 0.12s

Iterate on integration tests but also have at the end of your session / context limit a e2e test run to pass.

---

Iterate from a todo list to any app. Use this repo as a base.
