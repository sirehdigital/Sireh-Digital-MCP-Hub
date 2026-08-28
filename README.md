# Sireh Digital MCP Hub

Central governance, registry, integration and reference repository for Model Context Protocol (MCP) services used across the Sireh Digital ecosystem.

> **Repository status:** Foundation / v0.1
> **Visibility:** Public
> **Security rule:** Never commit API keys, access tokens, passwords, private certificates, session cookies, `.env` files containing secrets, or customer/personal data.

## Purpose

This repository provides one canonical place to document:

- approved MCP servers and connectors;
- ownership, purpose and deployment status;
- integration patterns for Sireh Digital projects;
- security and governance requirements;
- reusable MCP configuration templates without secrets;
- operational runbooks and examples;
- skills that consume MCP capabilities.

## Sireh Digital ecosystem

The MCP Hub is designed to support the wider Sireh Digital architecture:

- **SAIL** — R&D / experimentation
- **SACReS** — research
- **SACHI** — intelligence
- **SAIE** — AI engine
- **SACP** — commerce platform
- **SirehLuxe** — commerce / launch use case
- Future products and business units such as JourneyMATE, WeddingMATE and SieWA

## Repository map

```text
Sireh-Digital-MCP-Hub/
├── README.md
├── SIREH_DIGITAL_MCP_HUB_ARCHITECTURE.md
├── MCP_REGISTRY.md
├── SECURITY.md
├── CONTRIBUTING.md
├── .gitignore
├── docs/
│   ├── ecosystem/
│   ├── architecture/
│   ├── governance/
│   └── integration-guides/
├── mcp/
│   ├── commerce/
│   ├── research/
│   ├── marketing/
│   ├── automation/
│   ├── development/
│   └── productivity/
├── configs/
│   ├── development/
│   ├── staging/
│   └── production/
├── skills/
│   ├── commerce/
│   ├── research/
│   ├── marketing/
│   └── operations/
└── examples/
```

## Core documents

| Document | Purpose |
|---|---|
| `SIREH_DIGITAL_MCP_HUB_ARCHITECTURE.md` | Canonical architecture and operating model |
| `MCP_REGISTRY.md` | Approved / planned MCP inventory |
| `SECURITY.md` | Security controls and secret-handling rules |
| `CONTRIBUTING.md` | Change, review and documentation standards |

## MCP onboarding lifecycle

1. **Discover** — identify a required MCP capability.
2. **Evaluate** — assess business value, permissions, data exposure and maintenance risk.
3. **Register** — add it to `MCP_REGISTRY.md`.
4. **Integrate** — document configuration and usage without committing secrets.
5. **Validate** — test least-privilege access and expected tool behaviour.
6. **Approve** — mark status as approved for the intended environment.
7. **Operate** — monitor, review and retire when no longer required.

## Initial MCP domains

- Commerce — Shopify and future commerce integrations
- Research — Firecrawl and research/data sources
- Marketing — Meta, content and campaign tooling
- Automation — Hermes and workflow orchestration
- Development — GitHub and engineering tools
- Productivity — collaboration and knowledge tools

## Configuration policy

Only templates and non-sensitive examples belong in this repository. Real credentials must be injected through an approved secret store, environment variables, local protected configuration or the hosting platform's secret-management facility.

Example:

```env
# SAFE TEMPLATE ONLY
SERVICE_API_KEY=${SERVICE_API_KEY}
SERVICE_BASE_URL=https://example.invalid
```

Never commit:

```env
SERVICE_API_KEY=real-secret-value
```

## Versioning

The repository begins at **Foundation v0.1**. Architecture decisions should be recorded as documentation changes and, as the system matures, through ADRs under `docs/architecture/`.

## Current priority

Build a governed MCP registry first, then connect MCP services to SAIE/SACP and other Sireh Digital products through reusable, secure integration patterns.
