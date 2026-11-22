# Cloud Wise

Standardized infrastructure portal. A fullstack monorepo for Azure provisioning (RunOps) and cost visibility (Cloud Wise).

## Stack

| Layer | Technologies |
|-------|--------------|
| Backend | Python 3.12, FastAPI, DDD, SQLModel, Pulumi |
| Frontend | React 19, Vite, TanStack Router/Query/Form, Valibot, Tailwind v4 |
| Infra | Pulumi Azure Native, Docker Compose (SQL Server) |

## Quick start

```bash
cp .env.example .env
docker compose up -d

# Backend
cd backend
poetry install
poetry run alembic upgrade head                        # creates the tables and the template catalog
env PYTHONPATH=src poetry run python -m infra.database.seed   # demo data (dev only)
poetry run uvicorn infra.http.main:app --reload --app-dir src --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

- API: http://localhost:8000/api/v1/health
- UI: http://localhost:5173

Tests: `cd backend && poetry run pytest` and `cd frontend && npm test`.

## Roles and authentication

Easy Auth (Azure App Service) authenticates; authorization lives in the `users` table.

| Role | Can |
|------|-----|
| `runops.viewer` (default on first login) | see the dashboard, costs and their own requests |
| `runops.provisioner` | everything a viewer can, plus create provisioning requests |
| `runops.admin` | everything, plus see all requests and manage users (role, block) |

- The first admin comes from `ADMIN_EMAILS` in `.env` (comma-separated emails).
- Roles carried in the Entra ID token are ignored.
- **Local development:** with `APP_ENV=development` the backend accepts the `X-Dev-User-Id` and
  `X-Dev-User-Email` headers. The demo seed creates three users: `dev-viewer`, `dev-provisioner` and
  `dev-user` (admin). The frontend shows a user selector in the header (only in `npm run dev`) that
  picks which of them it sends (see `frontend/src/core/dev-users.ts`). Roles are never overwritten by
  the seed, so a promotion done in the **Users** page survives restarts. Outside `development` the
  headers are ignored.
- Outside `development`, `SECRET_KEY` and `PULUMI_CONFIG_PASSPHRASE` are required; the app won't start without them.
- The schema is versioned with Alembic (`backend/alembic/`). `alembic upgrade head` builds it and loads
  the template catalog; `alembic downgrade base` removes it. The demo seed (sample costs and dev users)
  is a separate command that refuses to run outside `development`. To start from scratch:
  `docker compose down -v && docker compose up -d` (the `db-init` service creates the `cloudwise`
  database), then the commands above.

## Docs

- [Architecture](docs/architecture.md)
- [Smoke test](docs/smoke-test.md)

## Layout

```
backend/src/   core, domain, infra (DDD)
frontend/src/  core, ui, layouts, features, routes
infra/pulumi/  Pulumi program: Resource Group + Storage Account or Key Vault
```
