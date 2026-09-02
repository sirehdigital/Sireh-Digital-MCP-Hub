# Staging Configuration

Safe configuration templates for constrained pre-production validation.

Staging should use dedicated credentials and narrower permissions than production wherever possible.

`mcp-core.json` disables writes, external side effects and runtime health probes by default. Server-level `enabled` flags still apply.
