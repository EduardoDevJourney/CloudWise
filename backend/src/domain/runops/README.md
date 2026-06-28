# RunOps — Core Subdomain

Provisionamento de recursos Azure via Pulumi Automation API.

## Entidades

- `ProvisionRequest` (aggregate root) — ciclo de vida: pending → running → success/failed
- `Template` — catálogo de recursos autorizados

## Value Objects

- `ProvisionStatus`

## Domain Events

- `ProvisionRequestedEvent`
- `ProvisionCompletedEvent`
- `ProvisionFailedEvent`
