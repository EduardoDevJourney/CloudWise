# Architecture

Monorepo with a FastAPI backend (DDD) and a React frontend.

```
backend/     FastAPI API and DDD domain
frontend/    React 19 SPA
infra/       Pulumi programs
docs/
docker-compose.yml   local SQL Server
```

## RunOps flow

1. `POST /api/v1/runops/provision` checks the role and the naming policy, then stores the request as `PENDING`.
2. A background task runs Pulumi `up()`.
3. The request ends as `SUCCESS` (with the stack outputs) or `FAILED` (with a short error summary).
4. The frontend re-fetches `GET /api/v1/runops/requests` every few seconds while any request is still active.

## Backend subdomains

- **runops** (core): Pulumi provisioning
- **cloudwise** (supporting): costs and dashboard
- **auth** (generic): Easy Auth adapter and the users table that holds roles

## Frontend layers

`core` → `ui` → `layouts` → `features` → `routes`

Imports only go in that direction; `eslint-plugin-boundaries` enforces it.
