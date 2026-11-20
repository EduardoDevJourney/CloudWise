# Arquitetura Cloud Wise

## Visão Geral

Monorepo com backend FastAPI (DDD) e frontend React (camadas TanStack).

```
cloud-wise/
├── backend/     # API FastAPI + domínio DDD
├── frontend/    # SPA React 19
├── infra/       # Programas Pulumi
├── docs/        # Documentação
└── docker-compose.yml  # SQL Server local
```

## Fluxo RunOps

1. `POST /api/v1/runops/provision` → valida RBAC, salva `PENDING`
2. Background job executa Pulumi `up()`
3. Status atualizado para `SUCCESS` ou `FAILED`
4. Frontend faz polling em `GET /api/v1/runops/status/{id}`

## Subdomínios Backend

- **runops** (core) — provisionamento Pulumi
- **cloudwise** (supporting) — custos e dashboard
- **auth** (generic) — Easy Auth adapter

## Camadas Frontend

`core` → `ui` → `pattern` → `layouts` → `features` → `routes`
