# Architectural Decisions — Backend

## Sprint 1 — MVP Foundation

- **Stack:** Python 3.12+, FastAPI, Poetry, SQLModel, Pulumi Automation API
- **Arquitetura:** DDD + Clean Architecture (`core` / `domain` / `infra`)
- **Erros:** Padrão Either — use cases retornam `Left(Error)` ou `Right(Result)`
- **Auth:** Easy Auth via middleware na infra; headers dev em local
- **DB:** SQL Server local (Docker) → Azure SQL em produção
- **Bounded Contexts:** `runops`, `cloudwise`

## Modelo de custos

- Custos usam esquema estrela (`fact_custo` + `dim_data`, `dim_servico`, `dim_assinatura`): é o lado
  analítico e cresce para novos relatórios. O lado operacional (users, templates, solicitações)
  continua normalizado por ser transacional.
- Filtros e agregações rodam em SQL (joins e `GROUP BY`) no `SQLCostsRepository`.

## Migrações

- Schema versionado com Alembic; a API não cria nem altera tabelas na subida.
- Dados de referência (catálogo de templates) entram por migração de dados; dados de demonstração
  (custos de exemplo e usuários de teste) por comando explícito, só em `development`.

## Integrações Externas

- Azure Easy Auth (headers `X-MS-CLIENT-PRINCIPAL*`)
- Pulumi Automation API (provisionamento RG + Storage)
- Azure Cost Management API — **fase 2** (ETL)
