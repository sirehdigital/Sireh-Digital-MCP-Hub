# ADR-0001: MCP Core v0.1 Contracts

Status: Accepted
Date: 2026-09-02

## Decision

Use JSON as the canonical machine-readable format, Python standard library for validation, explicit server/client allowlists, four permission classes and default-disabled external registrations.

## Rationale

JSON is deterministic and consumable by Codex, Hermes and future SAIE/SACP components. Standard-library validation avoids a package-install or supply-chain dependency at the foundation checkpoint. Default-disabled registrations preserve the existing integration inventory without implying live readiness.

## Consequences

- Markdown remains a human-readable view, not the machine source of truth.
- Runtime connectivity is optional and distinct from contract validity.
- More complete JSON Schema enforcement or signed policy bundles can be considered in v0.2.
- Composio remains outside the v0.1 boundary.
