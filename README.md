# Sireh Digital MCP Hub

**Sireh Digital MCP Core v0.1.0 — VERIFIED FOUNDATION**

The Sireh Digital MCP Hub is the central registry, governance and interoperability layer for MCP servers, clients and approved tool access across the Sireh Digital ecosystem. It records what may connect, who owns it, which environment may use it, the permitted capabilities and when Founder approval is required.

> Public-repository rule: never commit API keys, access tokens, passwords, private certificates, session cookies, production endpoints containing credentials, customer data or real `.env` values.

## Architectural role

```text
Founder / Seri
      ↓
Sireh Digital MCP Hub
      ↓
SAIE / SACP / future systems
      ↓
Codex / Hermes / agents
      ↓
Approved tools and external services
```

The diagram expresses the governance path: Founder authority is encoded by the Hub, future orchestration systems consume that policy, clients act within it, and only registered tools are exposed.

- **MCP Hub ≠ SAIE.** SAIE is the future AI reasoning and orchestration layer.
- **MCP Hub ≠ SACP.** SACP is the commerce control and execution platform.
- **MCP Hub ≠ Composio.** Composio is a possible future integration provider and is explicitly out of scope for v0.1.
- **MCP Hub = controlled interoperability and tool governance.**

Future direction, not v0.1 implementation:

```text
Sireh Digital MCP → SAIE → SACP → Hermes → Composio later
```

## v0.1 scope

MCP Core v0.1 provides:

- a machine-readable server registry at `registry/mcp-registry.json`;
- a machine-readable client registry at `registry/clients.json`;
- JSON schemas for server registry, client registry and audit-event contracts;
- READ_ONLY, LOW_RISK_WRITE, APPROVAL_REQUIRED and RESTRICTED policy classes;
- conservative development, staging and production configuration;
- safe Codex/Suri and Hermes/Miss Hermes examples;
- a dependency-free registry, configuration, audit-example and secret-pattern validator;
- a default-deny, non-executing permission decision command;
- opt-in HTTP/process readiness checks for enabled servers.

All external server entries are disabled by default. v0.1 validates governance and configuration; it does not connect live accounts or prove third-party service availability.

## Repository map

```text
Sireh-Digital-MCP-Hub/
├── registry/                 # machine-readable servers and clients
├── schemas/                  # registry and audit-event contracts
├── scripts/                  # validation/readiness command
├── tests/                    # standard-library tests
├── configs/                  # development/staging/production defaults
├── docs/                     # architecture, governance and guides
├── examples/                 # secret-free registrations and client configs
├── mcp/                      # domain-specific MCP documentation
├── skills/                   # skills that consume governed MCPs
├── MCP_REGISTRY.md           # human-readable registry view
├── SECURITY.md
└── SIREH_DIGITAL_MCP_HUB_ARCHITECTURE.md
```

## Validate MCP Core

Requires Python 3.10+ and no third-party packages.

```bash
python3 scripts/validate_registry.py
python3 -m unittest discover -s tests -v
```

Permission decisions can be tested without calling a tool:

```bash
python3 scripts/check_permission.py --client CLIENT-CODEX-SURI --server MCP-RES-001 --capability web.search --environment development
```

For enabled servers whose health checks are explicitly configured, runtime probing is opt-in:

```bash
python3 scripts/validate_registry.py --check-runtime --json
```

The normal validator checks JSON loading, required fields, IDs, enums, environment conventions, server/client references, documentation paths, conservative production defaults, audit-event consistency and obvious committed-secret signatures. Disabled servers report `DISABLED`; this is an expected safe state, not a connectivity failure.

## Registration workflow

1. Define the server in `registry/mcp-registry.json` with `enabled: false`.
2. Document its ownership, transport, environment-variable names, capabilities, risk and health policy.
3. Add it to a client allowlist in `registry/clients.json` only when needed.
4. Run validation and review the permission boundary.
5. Obtain Founder approval for sensitive or consequential access.
6. Inject credentials outside this repository and enable only in the approved environment.
7. Record tool use using the audit-event contract.

See `docs/integration-guides/REGISTRATION.md` for examples and discovery rules.

## MCP Core v0.1 acceptance criteria

- [x] Registry is machine-readable and validates
- [x] Server registration convention exists
- [x] Client registration convention exists
- [x] Permission classes exist
- [x] Security rules are documented
- [x] Health/readiness validation works
- [x] Audit-event schema exists
- [x] Development/staging/production conventions exist
- [x] Codex/Suri example exists
- [x] Hermes/Miss Hermes example exists
- [x] No secrets are committed
- [x] Validation and tests pass
- [x] README accurately describes the architecture

## Boundaries

- Composio integration is on hold.
- SAIE and SACP code are not part of this repository and are not modified by MCP Core v0.1.
- A registry entry is not production approval.
- `RESTRICTED` actions are never delegated through a normal client profile.
- Founder approval remains authoritative for publishing, sending, live-system mutation, commerce configuration, payments, customer data, production secrets and destructive actions.

## Versioning

`VERSION` is the source of the repository checkpoint version. Registry/schema contract changes should use semantic versioning and architecture decisions should be recorded under `docs/architecture/`.
