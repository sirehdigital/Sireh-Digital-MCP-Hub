# Production Configuration

Public-safe documentation for production configuration shape only.

Never commit production credentials, tokens, private endpoints, customer data or sensitive operational values to this directory.

`mcp-core.json` is conservative: writes, external side effects and runtime probes default to false, while Founder approval and audit logging default to true.
