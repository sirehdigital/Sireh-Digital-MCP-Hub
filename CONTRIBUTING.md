# Contributing to Sireh Digital MCP Hub

This repository is documentation-first. Changes should improve clarity, security, interoperability and governance.

## Contribution principles

- Never commit secrets or sensitive customer data.
- Prefer small, reviewable changes.
- Document the business purpose of new MCP integrations.
- Separate verified facts from planned architecture.
- Use least-privilege assumptions.
- Mark unverified integrations as `PLANNED` or `EVALUATING`.
- Keep examples vendor-neutral where practical.

## Adding a new MCP

1. Add or update the entry in `MCP_REGISTRY.md`.
2. Create a domain document under `mcp/<domain>/`.
3. Document authentication type and required scopes without secret values.
4. Identify projects and environments that will use it.
5. Assign a risk tier.
6. Define whether human approval is required for writes.
7. Add a safe example under `configs/` or `examples/` if useful.
8. Update architecture docs if the integration changes system boundaries.

## Documentation standard

A connector document should normally contain:

```text
Name
MCP ID
Status
Purpose
Provider
Projects
Environments
Authentication
Required scopes
Tools/capabilities
Read/write behaviour
Risk tier
Approval boundary
Configuration template
Validation checklist
Operational notes
```

## Commit conventions

Recommended prefixes:

- `docs:` documentation and registry
- `feat:` new integration pattern or implementation
- `security:` security or permission hardening
- `config:` safe configuration templates
- `chore:` repository maintenance
- `fix:` correction to existing material

Examples:

```text
docs: register Shopify MCP
security: document Meta permission boundary
config: add Firecrawl development template
```

## Production readiness

Do not label an MCP `APPROVED-PROD` merely because it connects successfully. Production approval should include permission review, failure behaviour, ownership and test evidence.

## Deprecation

When retiring an MCP:

- change registry status to `RETIRED`;
- record replacement where applicable;
- remove obsolete example configuration;
- revoke unused credentials outside this repository;
- preserve relevant architecture history.
