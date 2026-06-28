# Cloud Wise — Cloud Proxy MVP

Monorepo fullstack para provisionamento Azure (RunOps) e visualização de custos (Cloud Wise).

## Stack

| Camada | Tecnologias |
|--------|-------------|
| Backend | Python 3.12, FastAPI, DDD, SQLModel, Pulumi |
| Frontend | React 19, Vite, TanStack Router/Query/Form, Valibot, Tailwind v4 |
| Infra | Pulumi Azure Native, Docker Compose (SQL Server) |

## Início rápido

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

## Documentação

- [Plano completo](plan.md)
- [Arquitetura](docs/architecture.md)
- [Smoke test](docs/smoke-test.md)
- [Backend DDD guide](backend.md)
- [Frontend architecture guide](front-end.md)

## Estrutura

```
backend/src/   → core, domain, infra (DDD)
frontend/src/  → core, ui, features, routes
infra/pulumi/  → RG + Storage Account
```
