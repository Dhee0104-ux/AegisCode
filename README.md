# AegisCode
Autonomous Multi-Agent Software Engineering Platform.

A production-oriented starter platform that turns a natural-language requirement into a structured project specification, architecture, dependency-aware task graph, generated workspace, tests, security report, documentation and deployment artifacts. It uses FastAPI + WebSockets, a React/Vite frontend, SQLite for local persistence, an optional OpenAI-compatible LLM, and Docker sandbox execution.

## Quick start

### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

### Optional LLM
Copy `.env.example` to `.env` and set `LLM_API_KEY`, `LLM_BASE_URL`, and `LLM_MODEL`. Without an LLM, AegisCode uses deterministic local agents so the platform remains runnable.

### Docker sandbox
Docker must be installed and the daemon available. The sandbox is opt-in per run and never executes generated commands on the host. On systems without Docker, the API reports sandbox-unavailable instead of falling back to host execution.

### Full stack
```bash
docker compose up --build
```
Frontend: http://localhost:5173, backend: http://localhost:8000.

## Workflow
Analyst -> Architecture -> Planner -> Coder -> Tester -> Debugger (bounded repair loop) -> Security -> Documentation -> Deployment.

Every transition and file change is persisted in the audit log. Project workspaces are isolated under `backend/projects/<project_id>/`.
