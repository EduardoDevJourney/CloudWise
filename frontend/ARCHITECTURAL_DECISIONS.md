# Architectural Decisions — Frontend

## Sprint 1 — MVP Foundation

- **Stack:** React 19, Vite, TypeScript strict, TanStack Router/Query/Form, Valibot, Tailwind v4, MSW
- **Arquitetura:** `core` / `ui` / `pattern` / `layouts` / `features` / `routes`
- **Server state:** TanStack Query com `refetchInterval` para polling RunOps
- **Forms:** TanStack Form + Valibot schemas
- **HTTP:** Cliente centralizado em `core/http-resource.ts`
- **Boundaries:** `eslint-plugin-boundaries` entre camadas

## Contratos de Dados

Tipos em `core/api/` espelham endpoints do backend Cloud Wise (RunOps + Cloud Wise).
