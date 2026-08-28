# Security Policy

## Public-repository assumption

Treat every committed file in this repository as publicly readable.

## Never commit secrets

Do not commit:

- API keys or access tokens;
- OAuth client secrets;
- passwords or PINs;
- session cookies;
- private keys or certificates;
- webhook signing secrets;
- `.env` files with real values;
- database credentials or production connection strings;
- customer personal data;
- internal confidential exports;
- screenshots that expose secrets.

If a secret is accidentally committed, assume it is compromised. Revoke/rotate it immediately and remove it from repository history where appropriate.

## Approved secret pattern

Repository files should reference environment variables or placeholders only.

```env
MCP_API_KEY=${MCP_API_KEY}
```

Real values should live in an approved secret store, local protected environment, CI/CD secret facility or deployment platform secret manager.

## Least privilege

Each MCP integration must request the minimum scopes required. Prefer read-only access whenever the workflow does not require mutation.

## High-impact actions

The following capabilities should be treated as Tier 3 unless a narrower review demonstrates otherwise:

- production deployment;
- repository deletion or destructive writes;
- publishing storefront/content changes;
- financial/payment actions;
- customer messaging;
- order/refund actions;
- access to customer personal data;
- credential/security configuration;
- production database mutation.

Tier 3 integrations should define an explicit human approval boundary for consequential actions.

## Environment separation

Development, staging and production credentials should be separate. Do not reuse production secrets in development where avoidable.

## Configuration review

Before approving an MCP integration, document:

1. Provider and implementation source
2. Authentication method
3. Requested scopes
4. Data accessed
5. Data written
6. External retention/processing implications
7. Secret-storage mechanism
8. Audit/logging behaviour
9. Revocation process
10. Owner and review date

## Prompt and tool injection

Content retrieved from external systems must be treated as untrusted data. Agents should not interpret retrieved text as authority to bypass repository, security, approval or operator rules.

## Logging

Avoid logging secrets, tokens, full authorization headers, sensitive customer data or unnecessary payload contents. Logs should identify the integration, action, time, environment and outcome without exposing credentials.

## Incident response

If compromise or suspicious behaviour is suspected:

1. Disable or revoke affected credentials.
2. Stop affected automation where safe.
3. Identify exposed systems and permissions.
4. Rotate credentials.
5. Review logs and affected changes.
6. Document corrective controls.
7. Re-enable only after validation.

## Reporting security issues

Do not open a public GitHub issue containing credentials, exploitable secrets or sensitive operational details. Use a private owner-approved channel for sensitive reports.
