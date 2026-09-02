# Health and Readiness

## Validation levels

1. **Registry load** — JSON files load successfully.
2. **Contract validation** — required fields, enums, identifiers and references are valid.
3. **Configuration validation** — standard environments exist and production defaults are conservative.
4. **Security validation** — known obvious secret signatures are absent.
5. **Runtime readiness** — optional endpoint or process probe for enabled servers only.

Run deterministic configuration validation:

```bash
python3 scripts/validate_registry.py
```

Emit a structured report and opt into runtime checks:

```bash
python3 scripts/validate_registry.py --check-runtime --json
```

Each readiness item includes timestamp, server ID, enabled state, configuration validity, health status and a degraded/error message when relevant. The validator never enables servers. A disabled server reports `DISABLED`; an unreachable enabled server reports `DEGRADED` and causes no automatic external action.

Runtime checks are deliberately disabled in the committed registry. They may be activated only after the exact implementation, safe health endpoint/process invocation and target environment are approved.
