# MCP Server and Client Registration

## Registration model

`registry/mcp-registry.json` records MCP servers. It supports internal Sireh Digital servers, external providers, and future SAIE/SACP tools without coupling the Hub to those systems. `registry/clients.json` records Codex/Suri, Hermes/Miss Hermes, ChatGPT/Seri where applicable, and future local agents.

Registration is metadata and policy only. It does not install a package, start a process, exchange credentials or connect an account.

## Register a server

1. Allocate `MCP-<DOMAIN>-<NUMBER>` using the codes in `MCP_REGISTRY.md`.
2. Add every required field using `examples/mcp-registration.example.yaml` as the shape.
3. Use only `${VARIABLE_NAME}` for a command or endpoint and list credential variable names without values.
4. Start with `enabled: false` and `status: DRAFT` or `REGISTERED`.
5. Enumerate capabilities narrowly and choose the highest applicable risk class.
6. Create or reference a documentation file.
7. Add an opt-in health check and run the validator.

An external MCP server normally points to a provider-controlled endpoint. An internal server normally uses an approved local command or private endpoint. Future SAIE/SACP tool servers follow the same contract but remain disabled until their separate code, authentication and environment are verified.

## Register a client

1. Allocate a stable `CLIENT-*` ID.
2. Set its permitted environments and default enabled state.
3. Add only required MCP IDs to `server_allowlist`.
4. Grant only required risk classes; never grant `RESTRICTED`.
5. Keep Founder as approval authority for consequential actions.
6. Point to a secret-free client example or guide.

## Discovery example

A client must not scan for arbitrary servers. It loads the canonical registries, finds its exact client ID, intersects the client allowlist with servers enabled for the current environment, and filters requested capabilities by risk policy.

```python
servers = load("registry/mcp-registry.json")["servers"]
clients = load("registry/clients.json")["clients"]
client = find(clients, id="CLIENT-CODEX-SURI")
available = [
    server for server in servers
    if server["id"] in client["server_allowlist"]
    and server["enabled"]
    and CURRENT_ENV in server["environment"]
    and server["risk_class"] in client["allowed_risk_classes"]
]
```

Before execution, the client still performs the permission decision in `docs/governance/PERMISSION_POLICY.md`. Server discovery never bypasses Founder approval.

## Safe configuration examples

- Codex/Suri: `examples/codex-suri.mcp.example.json`
- Hermes/Miss Hermes: `examples/hermes-miss-hermes.mcp.example.json`

Both examples use environment-variable names, explicit enable/disable controls and least-privilege limits. They are intentionally non-live.
