# Plano Do MVP Cloud Proxy

> Monorepo fullstack: backend Python/FastAPI (DDD), frontend React 19 (TanStack), SQL Server local, Cloud Wise mockado, RunOps com Pulumi na sandbox Azure.

## Documentos De Referência

- [`backend.md`](backend.md) — DDD + Clean Architecture
- [`front-end.md`](front-end.md) — camadas SPA + TanStack stack
- Blueprint PDF — módulos RunOps e Cloud Wise

## Decisões Fechadas

| Tópico | Decisão |
|--------|---------|
| Backend | Python 3.12+ / FastAPI / Poetry / SQLModel / Alembic |
| Arquitetura backend | DDD: `core` → `domain` → `infra` |
| Frontend | React 19 + Vite + TanStack Router/Query/Form + Valibot + Tailwind v4 |
| Auth | Easy Auth via middleware; dev com headers simulados |
| Erros | Padrão Either (`Left`/`Right`) |
| Pulumi | RG + Storage Account, state local |
| Cloud Wise MVP | Dados mockados/seedados |

## Commits Atômicos (29)

### Fase 0 — Fundação
1. `chore: add monorepo structure and gitignore`
2. `chore: add docker compose for local sql server`
3. `docs: add architectural decisions skeleton`

### Fase 1 — Backend core e domínio
4. `feat(backend): add core either entity and event foundations`
5. `feat(backend): add runops domain entities and value objects`
6. `feat(backend): add cloudwise domain entities`
7. `feat(backend): add domain events for provision lifecycle`

### Fase 2 — Backend infra e persistência
8. `feat(backend): scaffold fastapi with ddd folder structure`
9. `feat(backend): add database config and sqlmodel models`
10. `chore(backend): configure alembic and initial migration`
11. `feat(backend): add in-memory and sqlmodel repositories`

### Fase 3 — Backend use cases e HTTP
12. `feat(backend): add runops use cases with either pattern`
13. `feat(backend): add cloudwise use cases with either pattern`
14. `feat(backend): add easy auth middleware and rbac adapter`
15. `feat(backend): add fastapi controllers and dtos`

### Fase 4 — Pulumi e jobs
16. `feat(infra): add pulumi program for resource group and storage`
17. `feat(backend): add pulumi adapter and background provision job`
18. `feat(backend): add seed data for templates and mock costs`

### Fase 5 — Frontend fundação
19. `feat(frontend): scaffold react 19 vite with layered architecture`
20. `feat(frontend): add eslint boundaries and vitest setup`
21. `feat(frontend): add ui primitives and pattern form layer`
22. `feat(frontend): add http-resource api client and query architecture`
23. `feat(frontend): add msw mocks and auth provider`

### Fase 6 — Frontend features
24. `feat(frontend): add layouts and tanstack router bootstrap`
25. `feat(frontend): add cloudwise feature and dashboard route`
26. `feat(frontend): add runops provision form and request list`
27. `feat(frontend): add runops status polling via tanstack query`
28. `chore(frontend): wire runops route and navigation`

### Fase 7 — Documentação
29. `docs: add smoke test checklist and update living docs`

## Status Da Implementação

| Fase | Status |
|------|--------|
| 0 — Fundação monorepo | Concluída |
| 1-4 — Backend DDD + API + Pulumi | Concluída |
| 5-6 — Frontend camadas + features | Concluída |
| 7 — Documentação | Concluída |

### Commits realizados

1. `chore: add monorepo structure and gitignore`
2. `chore: add docker compose for local sql server`
3. `docs: add architectural decisions skeleton`
4. `feat(backend): add core ddd foundations`
5. `feat(backend): add runops and cloudwise domain layer`
6. `feat(backend): add fastapi infrastructure persistence and pulumi adapter`
7. `feat(frontend): add react 19 spa with layered architecture`
8. `docs: add plan, readme, smoke test and architecture guides`

## Como Executar

```bash
cp .env.example .env
docker compose up -d

# Backend (requer Poetry)
cd backend && poetry install
poetry run uvicorn infra.http.main:app --reload --app-dir src --port 8000

# Frontend
cd frontend && npm install && npm run dev
```

- API: http://localhost:8000/api/v1/health
- UI: http://localhost:5173/dashboard

## Critério De Pronto

1. `docker compose up` sobe SQL Server local
2. Backend com migrations e seed
3. Frontend consome API
4. Dashboard Cloud Wise com dados mockados
5. RunOps provisiona RG+Storage via Pulumi
6. Polling `pending → running → success/failed`
7. Use cases testados com in-memory repos
8. Living docs atualizados
