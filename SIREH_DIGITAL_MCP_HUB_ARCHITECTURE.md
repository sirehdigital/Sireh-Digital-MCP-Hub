# Sireh Digital MCP Hub Architecture

Version: 0.1.0
Status: VERIFIED FOUNDATION

## 1. Mission

The Sireh Digital MCP Hub is the canonical control plane for documenting, governing and standardising MCP integrations across Sireh Digital.

It is not a secret store and should not become a dumping ground for connector-specific credentials. Its role is to define what connects, why it connects, what permissions it needs, who owns it and how it is used safely.

## 2. Architectural position

```text
Business / Products
        |
        v
Agents & AI Experiences
(ChatGPT/Seri, Suri/Codex, Hermes, creative agents)
        |
        v
Sireh Digital MCP Hub
(registry + governance + integration contracts)
        |
        +-------------------------------+
        |        |        |             |
        v        v        v             v
   Commerce   Research  Marketing   Development/Automation
        |        |        |             |
        v        v        v             v
 Shopify     Firecrawl   Meta        GitHub / workflow tools
```

The Hub supports the broader Sireh Digital stack:

- SAIL — research and development
- SACReS — research collection
- SACHI — intelligence and synthesis
- SAIE — AI engine and reasoning/orchestration layer
- SACP — commerce execution layer

## 3. Design principles

### 3.1 Registry before integration
Every MCP must have an explicit registry entry before it is treated as part of the production architecture.

### 3.2 Least privilege
Grant only the minimum scopes required for the intended workflow. Separate read-only and write-capable integrations where possible.

### 3.3 Human approval for consequential actions
High-impact actions such as publishing, payment changes, customer messaging, destructive operations, deployment and irreversible mutations should retain an approval boundary unless explicitly designed otherwise.

### 3.4 Public repo, zero secrets
This repository may be public. Therefore all committed content must be safe for public disclosure.

### 3.5 Reusable integration contracts
Projects should consume documented MCP capabilities rather than rebuilding ad-hoc integrations independently.

### 3.6 Observability and accountability
Important tool calls and autonomous workflows should be attributable to an agent, project, purpose and environment.

## 4. Logical layers

### Layer A — Business domains
Projects, products and operating companies that consume capabilities.

Examples: SirehLuxe, SACP, JourneyMATE, WeddingMATE and future Sireh Digital products.

### Layer B — Agent layer
AI agents and operator experiences that decide when tools are needed.

### Layer C — MCP governance layer
This repository. It stores machine-readable server/client registries, architecture rules, templates, runbooks and approved patterns.

### Layer D — MCP servers/connectors
Protocol endpoints that expose tools, resources and actions.

### Layer E — External systems
Shopify, GitHub, Meta, Firecrawl, cloud services, databases and other platforms.

## 5. MCP domain taxonomy

- `mcp/commerce/` — commerce, store, order and product systems
- `mcp/research/` — web research, intelligence and data acquisition
- `mcp/marketing/` — social, ads, content and campaign systems
- `mcp/automation/` — workflow, scheduling and agent automation
- `mcp/development/` — source control, deployment and engineering systems
- `mcp/productivity/` — collaboration, files, calendars and knowledge tools

## 6. Environment model

Three standard environments are recognised:

- Development — experimentation and local testing
- Staging — integration validation with constrained access
- Production — approved live workloads

Configuration examples live under `configs/`. Real secrets never do.

## 7. MCP registration fields

Every registry entry should include:

- MCP ID
- Name
- Domain
- Provider
- Purpose
- Business owner
- Technical owner
- Projects using it
- Environments
- Access mode: read / write / mixed
- Authentication method
- Required scopes
- Data sensitivity
- Approval status
- Last review date
- Documentation location
- Risk notes

## 8. Integration lifecycle

```text
Discover
  -> Security Review
  -> Register
  -> Prototype
  -> Validate
  -> Approve
  -> Deploy
  -> Observe
  -> Periodic Review
  -> Retire
```

## 9. Permission classes

### READ_ONLY
Search, inspect, list, retrieve and analyze.

### LOW_RISK_WRITE
Controlled drafts, audit logs and non-production files.

### APPROVAL_REQUIRED
Publishing, sending, live-system changes, commerce configuration and external side effects. Explicit Founder approval is required.

### RESTRICTED
Credentials, payments, customer data, production secrets, destructive actions and deletion. These capabilities are not granted through ordinary client profiles.

## 10. Initial target integrations

The first registry should prioritise MCPs already useful to Sireh Digital operations, including GitHub, Shopify, Firecrawl and Meta-related tooling where supported. Additional connectors should be registered only after their exact implementation and permissions are verified.

## 11. Future architecture

As SAIE matures, the MCP Hub can become the canonical capability catalogue used by an orchestration layer to answer three questions before any tool use:

1. Which MCP can perform this task?
2. Is this agent authorised to use it in this environment?
3. Does the action require human approval?

That pattern allows Sireh Digital to scale agents and products without losing governance.
