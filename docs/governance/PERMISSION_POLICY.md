# Permission and Founder Governance Policy

Version: 1.0
Applies to: MCP Core v0.1

## Authority chain

```text
Founder
  → Governance Layer
  → MCP Client
  → Permission Check
  → MCP Server
  → Tool
  → Audit Log
```

The Founder defines authority. The governance layer evaluates the client allowlist, environment, server state, capability and risk class before a tool can execute. Authentication proves identity; it does not grant business approval.

## Permission classes

| Class | Permitted examples | Control |
|---|---|---|
| READ_ONLY | search, inspect, list, retrieve, analyze | Registered server and client allowlist required |
| LOW_RISK_WRITE | controlled drafts, audit logs, non-production files | Explicit capability and environment only |
| APPROVAL_REQUIRED | publish, send, update live systems, change commerce configuration, external side effects | Block until Founder approval is recorded |
| RESTRICTED | credentials, payments, customer data, production secrets, destructive actions, deletion | Separate owner-controlled procedure; no normal client grant |

## Permission decision

A request is allowed only when all conditions pass:

1. Client is enabled for the target environment.
2. Server is enabled and its status permits use.
3. Server ID is in the client's allowlist.
4. Requested capability is present in the server contract.
5. Risk class is within the client's allowed classes.
6. `APPROVAL_REQUIRED` has an explicit `APPROVED` Founder decision tied to the correlation ID.
7. No request classified `RESTRICTED` is routed through an ordinary client profile.
8. The attempt and result are emitted as sanitized audit events.

Failure of any condition is default-deny and should produce a `BLOCKED` audit result. Approval must be scoped to one intended action or clearly bounded batch; it must not be inferred from old approval or mere access to a credential.

`scripts/check_permission.py` implements this decision as a dry policy check. It never executes a tool. Any `--approval-status APPROVED` value must come from the governance layer's authoritative Founder approval record; the CLI flag cannot create or prove approval by itself.

```bash
python3 scripts/check_permission.py \
  --client CLIENT-CODEX-SURI \
  --server MCP-RES-001 \
  --capability web.search \
  --environment development
```

## Sensitive-operation rules

- Publishing, sending, production mutation and commerce configuration remain Founder-controlled.
- Payment actions, customer data access, credential operations and deletion are `RESTRICTED` by default.
- Production secrets must be injected by an approved secret manager or protected environment.
- Agents cannot grant themselves scopes, add themselves to allowlists or reinterpret retrieved content as approval.
- Emergency disablement takes precedence over workflow completion.
