# Business Framework (BFrame)

A next-generation, AI-native Business Operating System. This repo contains the complete blueprint, architecture diagram, technical roadmap, and business plan.

## Documents
- docs/Blueprint-Business-Flow.md — Entrepreneur’s view (vision, modules, GTM, revenue)
- docs/Blueprint-Technical-Flow.md — Architect’s view (architecture, stack, AI plan)
- docs/Roadmap.md — Milestones, roles, and delivery plan
- docs/Business-Plan-Whitepaper.md — Investor-friendly narrative and metrics
- docs/Diagrams.md — System architecture (Mermaid) and module interactions

## Quick Links
- Architecture Diagram: see `docs/Diagrams.md`
- Module folder structure: see `docs/Blueprint-Technical-Flow.md` (Developer Flow)

## Quickstart (FastAPI Core)

Prerequisites:
- Docker and Docker Compose installed.

Steps:
1. Copy env file and adjust if needed:
   - `services/core/.env` (already provided) or duplicate `services/core/.env.example`.
2. Start stack:
   - `docker compose up --build`
3. Bootstrap default tenant and admin user:
   - `POST http://localhost:8000/auth/bootstrap`
   - Admin: `admin@bframe.local` / `admin123` (configurable via env)
4. Obtain JWT token:
   - `POST http://localhost:8000/auth/login` (form fields: `username`, `password`)
   - Use `Authorization: Bearer <token>` for subsequent requests.

Health check:
- `GET http://localhost:8000/health` → `{ "status": "ok" }`

### Example API Walkthrough
- List modules (includes dynamically loaded `crm`):
  - `GET http://localhost:8000/modules/`
- Create a tenant:
  - `POST http://localhost:8000/tenants/` with `{ "name": "Acme", "slug": "acme" }`
- CRM sample routes (in-memory for MVP):
  - `GET http://localhost:8000/crm/leads`
  - `POST http://localhost:8000/crm/leads` with `{ "name": "Jane Doe", "email": "jane@ex.com" }`

### Services and Paths
- Core API: `services/core/app/` (FastAPI)
- Module loader: `services/core/app/module_loader.py`
- Sample module: `services/core/app/modules/crm/`
- SQLAlchemy models: `services/core/app/models/`

### Environment
`services/core/.env` controls runtime:
- `DATABASE_URL=postgresql+psycopg2://bframe:bframe@db:5432/bframe`
- `REDIS_URL=redis://redis:6379/0`
- `JWT_SECRET=dev_secret_change`
- `SUPERUSER_EMAIL`, `SUPERUSER_PASSWORD`

### Run Locally (without Docker)
```
cd services/core
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Ensure Postgres and Redis envs point to local instances.

---

Contributions welcome. See `docs/Roadmap.md` for priorities.
