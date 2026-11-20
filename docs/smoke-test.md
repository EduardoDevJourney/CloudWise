# Smoke Test — Cloud Wise MVP

## Pré-requisitos

- Docker
- Python 3.12+ com Poetry
- Node.js 20+
- Azure CLI autenticado (para Pulumi real)

## Passos

1. `cp .env.example .env`
2. `docker compose up -d`
3. `cd backend && poetry install && poetry run uvicorn infra.http.main:app --reload --app-dir src --port 8000`
4. `cd frontend && npm install && npm run dev`
5. Abrir `http://localhost:5173/dashboard`
6. Verificar cards de custo mockados
7. Ir para `/runops` e provisionar template `rg-storage`
8. Acompanhar status na listagem

## Endpoints

- `GET /api/v1/health`
- `GET /api/v1/cloudwise/dashboard`
- `POST /api/v1/runops/provision`
- `GET /api/v1/runops/status/{id}`
