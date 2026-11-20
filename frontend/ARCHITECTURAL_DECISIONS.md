# Architectural decisions: frontend

- **Stack:** React 19, Vite, TypeScript strict, TanStack Router/Query/Form, Valibot, Tailwind v4, MSW
- **Layers:** `core` / `ui` / `layouts` / `features` / `routes`, enforced by `eslint-plugin-boundaries`
- **Server state:** TanStack Query; the request list refetches every few seconds while any request is still active
- **Forms:** TanStack Form. The resource name rule comes from the server policy (`GET /runops/policy`), so the
  backend stays the single source of the rules
- **HTTP:** one client in `core/http-resource.ts`

Types in `core/types/api.ts` mirror the backend DTOs, snake_case included.
