# Architectural Decisions — Backend

## Sprint 1 — MVP Foundation

- **Stack:** Python 3.12+, FastAPI, Poetry, SQLModel, Pulumi Automation API
- **Arquitetura:** DDD + Clean Architecture (`core` / `domain` / `infra`)
- **Erros:** Padrão Either — use cases retornam `Left(Error)` ou `Right(Result)`
- **Auth:** Easy Auth via middleware na infra; headers dev em local
- **DB:** SQL Server local (Docker) → Azure SQL em produção
- **Bounded Contexts:** `runops`, `cloudwise`

## Integrações Externas

- Azure Easy Auth (headers `X-MS-CLIENT-PRINCIPAL*`)
- Pulumi Automation API (provisionamento RG + Storage)
- Azure Cost Management API — **fase 2** (ETL)
