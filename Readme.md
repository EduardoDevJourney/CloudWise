# Cloud Wise — portal de infraestrutura padronizada

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

## Perfis e autenticação

O Easy Auth (Azure App Service) autentica; a autorização fica na tabela `users` do Cloud Wise.

| Papel | Pode |
|-------|------|
| `runops.viewer` (padrão no primeiro acesso) | ver dashboard, custos e as próprias solicitações |
| `runops.provisioner` | tudo do viewer + criar provisionamentos |
| `runops.admin` | tudo + ver todas as solicitações + gerenciar usuários (papel, bloquear) |

- O primeiro admin vem de `ADMIN_EMAILS` no `.env` (e-mails separados por vírgula).
- Os papéis que vêm no token do Entra ID são ignorados.
- **Desenvolvimento local:** com `APP_ENV=development` o backend aceita os headers `X-Dev-User-Id` e
  `X-Dev-User-Email`. O frontend envia `dev-user` / `dev-user@dev.local` (em `frontend/src/core/http-resource.ts`),
  que vira admin se estiver em `ADMIN_EMAILS`. Para testar outro perfil, troque o e-mail nesse arquivo (ele entra como
  viewer) e promova-o pela página **Usuários**. Fora de `development`, esses headers são ignorados.
- Fora de `development`, `SECRET_KEY` e `PULUMI_CONFIG_PASSPHRASE` são obrigatórios (a aplicação não sobe sem eles).
- Banco já existente: colunas novas são adicionadas automaticamente na subida (migração mínima).

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
