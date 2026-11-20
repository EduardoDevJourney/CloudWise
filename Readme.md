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
  `X-Dev-User-Email` headers. The frontend sends `dev-user` / `dev-user@dev.local`
  (see `frontend/src/core/http-resource.ts`), which becomes admin when listed in `ADMIN_EMAILS`.
  To try another profile, change the email in that file (it joins as viewer) and promote it from the
  **Users** page. Outside `development` these headers are ignored.
- Outside `development`, `SECRET_KEY` and `PULUMI_CONFIG_PASSPHRASE` are required; the app won't start without them.
- Existing databases get new nullable columns added on startup (minimal migration).

## Docs

- [Architecture](docs/architecture.md)
- [Smoke test](docs/smoke-test.md)

## Layout

```
backend/src/   core, domain, infra (DDD)
frontend/src/  core, ui, layouts, features, routes
infra/pulumi/  Pulumi program: Resource Group + Storage Account or Key Vault
```
