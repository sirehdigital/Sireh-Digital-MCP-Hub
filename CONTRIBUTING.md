# Contributing to Sireh Digital MCP Hub

This repository is documentation-first. Changes should improve clarity, security, interoperability and governance.

## Contribution principles

- Never commit secrets or sensitive customer data.
- Prefer small, reviewable changes.
- Document the business purpose of new MCP integrations.
- Separate verified facts from planned architecture.
- Use least-privilege assumptions.
- Mark unverified integrations as `DRAFT` or `REGISTERED` and keep them disabled.
- Keep examples vendor-neutral where practical.

## Adding a new MCP

1. Add or update the canonical entry in `registry/mcp-registry.json` and mirror its summary in `MCP_REGISTRY.md`.
2. Create a domain document under `mcp/<domain>/`.
3. Document authentication type and required scopes without secret values.
4. Identify projects and environments that will use it.
5. Assign a permission/risk class.
6. Define whether human approval is required for writes.
7. Add a safe example under `configs/` or `examples/` if useful.
8. Update architecture docs if the integration changes system boundaries.
9. Run `python3 scripts/validate_registry.py` and `python3 -m unittest discover -s tests -v`.

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
Permission/risk class
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

Do not label an MCP `READY` for production merely because it connects successfully. Production readiness requires permission review, failure behaviour, ownership, target-environment health evidence and Founder approval where applicable.

## Deprecation

When retiring an MCP:

- set `enabled: false` and change registry status to `DISABLED`;
- record replacement where applicable;
- remove obsolete example configuration;
- revoke unused credentials outside this repository;
- preserve relevant architecture history.
