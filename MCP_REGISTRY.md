# Sireh Digital MCP Registry

Version: 0.1
Status: Foundation register

This file is the canonical inventory of MCP services and connector capabilities approved, under evaluation or planned for the Sireh Digital ecosystem.

## Status values

- `PLANNED` — identified but not yet evaluated
- `EVALUATING` — security/capability review in progress
- `APPROVED-DEV` — approved for development only
- `APPROVED-STAGING` — approved for staging
- `APPROVED-PROD` — approved for production
- `HOLD` — temporarily paused
- `RETIRED` — no longer used

## Registry

| MCP ID | Name | Domain | Provider | Intended use | Access | Risk | Status | Projects |
|---|---|---|---|---|---|---|---|---|
| MCP-DEV-001 | GitHub | Development | GitHub | Repository, issue, PR and code workflows | Mixed | Tier 3 | EVALUATING | Sireh Digital engineering |
| MCP-RES-001 | Firecrawl | Research | Firecrawl | Web search, extraction and research workflows | Read / controlled write | Tier 2 | EVALUATING | SACReS, SACHI, SirehLuxe research |
| MCP-COM-001 | Shopify | Commerce | Shopify | Store, product, order and commerce workflows | Mixed | Tier 3 | PLANNED | SACP, SirehLuxe |
| MCP-MKT-001 | Meta Platform | Marketing | Meta | Social/marketing integrations where supported | Mixed | Tier 3 | PLANNED | SirehLuxe marketing |
| MCP-AUT-001 | Hermes | Automation | Sireh Digital | Local/agent workflow orchestration | Mixed | Tier 3 | PLANNED | Sireh Digital automation |

> The entries above are architecture placeholders until exact MCP implementation, authentication model and permission scopes are documented and verified.

## Required record template

Use this template when registering a new MCP.

```yaml
mcp_id: MCP-XXX-000
name: Example MCP
domain: research
provider: Example Provider
status: EVALUATING
purpose: Short description
business_owner: TBD
technical_owner: TBD
projects:
  - project-name
environments:
  - development
access_mode: read
risk_tier: Tier 1
authentication: OAuth2
required_scopes:
  - example.read
data_sensitivity: public
human_approval_required: false
documentation: mcp/research/example.md
last_reviewed: YYYY-MM-DD
notes: ""
```

## Approval checklist

Before changing an MCP to an approved state, verify:

- exact provider/server identity;
- official or trusted implementation source;
- authentication method;
- scopes/permissions;
- read/write behaviour;
- data categories exposed;
- external data retention implications;
- secret-storage method;
- rate limits and cost exposure;
- failure and rollback behaviour;
- human-approval requirements;
- project owner and technical owner;
- test evidence for the target environment.

## Naming convention

```text
MCP-<DOMAIN>-<NUMBER>
```

Domain codes:

- `COM` — Commerce
- `RES` — Research
- `MKT` — Marketing
- `AUT` — Automation
- `DEV` — Development
- `PRD` — Productivity
- `DAT` — Data / database
- `INF` — Infrastructure

## Review policy

Production MCP records should be reviewed when any of the following changes:

- provider or server implementation;
- authentication mechanism;
- requested permissions/scopes;
- data categories;
- business owner;
- production workflow;
- major version;
- security incident or material vulnerability.
