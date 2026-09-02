#!/usr/bin/env python3
"""Evaluate an MCP request against the v0.1 default-deny policy without executing it."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PERMITTED_SERVER_STATES = {"READY"}


def evaluate_permission(
    client: dict[str, Any] | None,
    server: dict[str, Any] | None,
    capability: str,
    environment: str,
    approval_status: str = "PENDING",
) -> dict[str, str]:
    """Return an ALLOW/BLOCK decision. The caller must source approval status authoritatively."""
    if client is None:
        return {"decision": "BLOCK", "reason": "unknown client"}
    if server is None:
        return {"decision": "BLOCK", "reason": "unknown server"}
    if not client.get("enabled"):
        return {"decision": "BLOCK", "reason": "client disabled"}
    if not server.get("enabled"):
        return {"decision": "BLOCK", "reason": "server disabled"}
    if server.get("status") not in PERMITTED_SERVER_STATES:
        return {"decision": "BLOCK", "reason": "server is not READY"}
    if environment not in client.get("environments", []):
        return {"decision": "BLOCK", "reason": "client not permitted in environment"}
    if environment not in server.get("environment", []):
        return {"decision": "BLOCK", "reason": "server not registered in environment"}
    if server.get("id") not in client.get("server_allowlist", []):
        return {"decision": "BLOCK", "reason": "server not in client allowlist"}
    if capability not in server.get("capabilities", []):
        return {"decision": "BLOCK", "reason": "capability not registered"}
    risk_class = server.get("risk_class")
    if risk_class == "RESTRICTED":
        return {"decision": "BLOCK", "reason": "RESTRICTED requires separate owner-controlled procedure"}
    if risk_class not in client.get("allowed_risk_classes", []):
        return {"decision": "BLOCK", "reason": "risk class not granted to client"}
    if risk_class == "APPROVAL_REQUIRED" and approval_status != "APPROVED":
        return {"decision": "BLOCK", "reason": "Founder approval not recorded"}
    return {"decision": "ALLOW", "reason": "all v0.1 permission checks passed"}


def load_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    servers = json.loads((ROOT / "registry/mcp-registry.json").read_text(encoding="utf-8"))["servers"]
    clients = json.loads((ROOT / "registry/clients.json").read_text(encoding="utf-8"))["clients"]
    return servers, clients


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", required=True, help="registered client ID")
    parser.add_argument("--server", required=True, help="registered MCP server ID")
    parser.add_argument("--capability", required=True, help="exact registered capability")
    parser.add_argument("--environment", required=True, choices=["development", "staging", "production"])
    parser.add_argument("--approval-status", default="PENDING", choices=["PENDING", "APPROVED", "DENIED", "NOT_REQUIRED"])
    args = parser.parse_args()
    servers, clients = load_records()
    client = next((item for item in clients if item["id"] == args.client), None)
    server = next((item for item in servers if item["id"] == args.server), None)
    decision = evaluate_permission(client, server, args.capability, args.environment, args.approval_status)
    print(json.dumps({
        "client": args.client,
        "server": args.server,
        "capability": args.capability,
        "environment": args.environment,
        **decision,
    }, indent=2))
    return 0 if decision["decision"] == "ALLOW" else 2


if __name__ == "__main__":
    sys.exit(main())
