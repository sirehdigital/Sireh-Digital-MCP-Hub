# Sireh Digital MCP Registry

Version: 0.1.0
Status: VERIFIED FOUNDATION

The canonical, machine-readable inventory is `registry/mcp-registry.json`. This document is its human-readable overview; update both in one change.

## Status values

- `DRAFT` — incomplete or not yet verified
- `REGISTERED` — contract recorded, but not runtime-ready
- `READY` — configuration and approved readiness checks pass for the stated environment
- `DEGRADED` — usable only with a recorded limitation or failed readiness check
- `DISABLED` — intentionally unavailable

## Risk classes

- `READ_ONLY` — search, inspect, list, retrieve and analyze
- `LOW_RISK_WRITE` — controlled drafts, logs and non-production files
- `APPROVAL_REQUIRED` — publishing, sending, live updates, commerce configuration and external side effects
- `RESTRICTED` — credentials, payments, customer data, production secrets, destructive actions and deletion

## Registered servers

| MCP ID | Name | Domain | Environments | Enabled | Risk | Status |
|---|---|---|---|---:|---|---|
| MCP-DEV-001 | GitHub MCP | development | development | No | APPROVAL_REQUIRED | REGISTERED |
| MCP-RES-001 | Firecrawl MCP | research | development | No | READ_ONLY | REGISTERED |
| MCP-COM-001 | Shopify MCP | commerce | development | No | APPROVAL_REQUIRED | DRAFT |
| MCP-MKT-001 | Meta Platform MCP | marketing | development | No | APPROVAL_REQUIRED | DRAFT |
| MCP-AUT-001 | Hermes MCP Gateway | automation | development | No | LOW_RISK_WRITE | DRAFT |

These records preserve the foundation inventory. They do not assert that an implementation package, endpoint, credential, scope or live connection has been verified. All remain disabled in v0.1.

## Required server contract

Every entry must include a stable ID, name, domain, owners, environments, environment-referenced transport locator, enabled state, authentication type, credential environment-variable names, capabilities, risk class, health check, version, status and existing documentation reference.

Client records and server allowlists are defined in `registry/clients.json`. See `docs/integration-guides/REGISTRATION.md` for the registration process.

## Approval rule

`READY` means validated for a named environment; it does not override approval. Any `APPROVAL_REQUIRED` operation must be blocked until Founder approval is recorded. `RESTRICTED` capabilities must not be granted through ordinary client registration.
