# Environment Configuration

MCP Core recognizes exactly three environments: `development`, `staging` and `production`. Each has a committed, secret-free policy file at `configs/<environment>/mcp-core.json`.

## Defaults

- Development may permit controlled local/non-production writes; external side effects remain disabled.
- Staging writes and external side effects default to disabled.
- Production writes and external side effects default to disabled, with Founder approval required.
- Server-level `enabled` flags are independent and take precedence.
- Runtime health checks are opt-in and do not grant permission.

## Secret names

Use uppercase names with underscores. Prefer:

- `<PROVIDER>_MCP_ENDPOINT` for HTTP/SSE locations;
- `<PROVIDER>_MCP_COMMAND` for an approved stdio launcher;
- `<PROVIDER>_MCP_TOKEN` for MCP-scoped bearer/OAuth material;
- `<PROVIDER>_API_KEY` only when the provider specifically uses API-key authentication.

Committed files contain only the variable name or `${VARIABLE_NAME}` reference. Real values belong in an approved secret store, protected local environment or deployment secret manager. Development, staging and production credentials must be separate.

`.env.example` is an inventory of names only. `.gitignore` blocks real `.env` variants, common key/certificate files, credential directories and generated audit output.
