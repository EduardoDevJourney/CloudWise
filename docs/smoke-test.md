# Smoke test

## Prerequisites

- Docker
- Python 3.12+ with Poetry
- Node.js 20+
- Azure service principal in `.env` (`AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`,
  `AZURE_SUBSCRIPTION_ID`) to run Pulumi for real

## Steps

1. `cp .env.example .env`
2. `docker compose up -d`
3. `cd backend && poetry install && poetry run alembic upgrade head`
4. `env PYTHONPATH=src poetry run python -m infra.database.seed` (demo costs and dev users)
5. `poetry run uvicorn infra.http.main:app --reload --app-dir src --port 8000`
6. `cd frontend && npm install && npm run dev`
7. Open `http://localhost:5173/dashboard` and check the cost cards and charts (sample data)
8. Go to `/runops` and provision the `rg-storage` template
9. Watch the request move through the list until it succeeds or fails

To rebuild the database from scratch: `docker compose down -v && docker compose up -d`, then steps 3 and 4.
`poetry run alembic current` and `poetry run alembic history` show the applied revisions;
`poetry run alembic downgrade base` followed by `upgrade head` is safe on a clean database.

## Endpoints

All under `/api/v1`.

| Route | Access |
|-------|--------|
| `GET /health` | open |
| `GET /me` | any authenticated user |
| `GET /users`, `PATCH /users/{id}` | admin |
| `POST /runops/provision` | provisioner or admin |
| `GET /runops/status/{id}` | owner or admin |
| `GET /runops/requests` | own requests (admin sees all) |
| `GET /runops/templates`, `GET /runops/policy` | authenticated |
| `GET /cloudwise/costs`, `GET /cloudwise/dashboard` | authenticated |

## Cost star schema demo

With the backend running, `GET /api/v1/cloudwise/dashboard?granularity=month` returns the same data
grouped by month. To show the schema in SQL Server:

```sql
SELECT d.ano_mes, s.nome AS servico, SUM(f.custo) AS total
FROM fact_custo f
JOIN dim_data d ON d.data_id = f.data_id
JOIN dim_servico s ON s.servico_id = f.servico_id
JOIN dim_assinatura a ON a.assinatura_id = f.assinatura_id
GROUP BY d.ano_mes, s.nome
ORDER BY total DESC;
```
