#!/usr/bin/env python3
"""Validate the Sireh Digital MCP Core registry with no third-party packages."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENTS = {"development", "staging", "production"}
DOMAINS = {"automation", "commerce", "data", "development", "infrastructure", "marketing", "productivity", "research"}
STATUSES = {"DRAFT", "REGISTERED", "READY", "DEGRADED", "DISABLED"}
RISK_CLASSES = {"READ_ONLY", "LOW_RISK_WRITE", "APPROVAL_REQUIRED", "RESTRICTED"}
APPROVAL_STATUSES = {"NOT_REQUIRED", "PENDING", "APPROVED", "DENIED"}
RESULTS = {"SUCCESS", "FAILURE", "BLOCKED", "DEGRADED"}
SERVER_REQUIRED = {
    "id", "name", "domain", "owner", "environment", "transport", "enabled",
    "authentication", "capabilities", "risk_class", "health_check", "version",
    "status", "documentation",
}
CLIENT_REQUIRED = {
    "id", "name", "owner", "type", "environments", "enabled", "server_allowlist",
    "allowed_risk_classes", "approval_authority", "documentation",
}
AUDIT_REQUIRED = {
    "timestamp", "event_id", "actor", "client", "server", "tool", "action",
    "environment", "risk_class", "approval_required", "approval_status", "result",
    "correlation_id", "error",
}
ENV_REFERENCE = re.compile(r"^\$\{[A-Z][A-Z0-9_]*\}$")
ENV_NAME = re.compile(r"^[A-Z][A-Z0-9_]*$")
MCP_ID = re.compile(r"^MCP-[A-Z]{3}-\d{3}$")
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "JWT": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
}


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)


def load_json(relative_path: str, validation: Validation) -> Any:
    path = ROOT / relative_path
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        validation.errors.append(f"{relative_path}: cannot load JSON: {exc}")
        return None


def validate_iso_timestamp(value: Any, field: str, validation: Validation) -> None:
    if not isinstance(value, str):
        validation.errors.append(f"{field}: expected ISO-8601 string")
        return
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        validation.errors.append(f"{field}: invalid ISO-8601 timestamp")


def validate_registry(data: Any, validation: Validation) -> set[str]:
    validation.require(isinstance(data, dict), "registry: root must be an object")
    if not isinstance(data, dict):
        return set()
    validation.require(data.get("schema_version") == "1.0.0", "registry: schema_version must be 1.0.0")
    validation.require(data.get("hub_version") == "0.1.0", "registry: hub_version must be 0.1.0")
    validation.require(set(data.keys()) == {"schema_version", "hub_version", "updated_at", "servers"}, "registry: unexpected or missing top-level fields")
    validate_iso_timestamp(data.get("updated_at"), "registry.updated_at", validation)
    servers = data.get("servers")
    validation.require(isinstance(servers, list), "registry.servers: must be an array")
    if not isinstance(servers, list):
        return set()

    ids: set[str] = set()
    for index, server in enumerate(servers):
        prefix = f"registry.servers[{index}]"
        validation.require(isinstance(server, dict), f"{prefix}: must be an object")
        if not isinstance(server, dict):
            continue
        missing = SERVER_REQUIRED - server.keys()
        validation.require(not missing, f"{prefix}: missing fields {sorted(missing)}")
        validation.require(set(server.keys()) == SERVER_REQUIRED, f"{prefix}: unexpected fields present")
        server_id = server.get("id")
        validation.require(isinstance(server_id, str) and bool(MCP_ID.fullmatch(server_id)), f"{prefix}.id: invalid MCP ID")
        validation.require(server_id not in ids, f"{prefix}.id: duplicate {server_id}")
        if isinstance(server_id, str):
            ids.add(server_id)
        validation.require(server.get("status") in STATUSES, f"{prefix}.status: invalid value")
        validation.require(server.get("risk_class") in RISK_CLASSES, f"{prefix}.risk_class: invalid value")
        validation.require(server.get("domain") in DOMAINS, f"{prefix}.domain: invalid value")
        environments = server.get("environment")
        validation.require(isinstance(environments, list) and bool(environments), f"{prefix}.environment: must be a non-empty array")
        if isinstance(environments, list):
            validation.require(set(environments) <= ENVIRONMENTS, f"{prefix}.environment: contains non-standard environment")
        validation.require(isinstance(server.get("enabled"), bool), f"{prefix}.enabled: must be boolean")
        capabilities = server.get("capabilities")
        validation.require(isinstance(capabilities, list) and bool(capabilities), f"{prefix}.capabilities: must be non-empty")

        owner = server.get("owner")
        validation.require(isinstance(owner, dict) and bool(owner.get("business")) and bool(owner.get("technical")), f"{prefix}.owner: business and technical owners required")
        transport = server.get("transport")
        validation.require(isinstance(transport, dict), f"{prefix}.transport: must be an object")
        if isinstance(transport, dict):
            kind = transport.get("type")
            validation.require(kind in {"stdio", "http", "sse"}, f"{prefix}.transport.type: invalid value")
            locator = transport.get("command") if kind == "stdio" else transport.get("endpoint")
            validation.require(isinstance(locator, str) and bool(locator), f"{prefix}.transport: command or endpoint required")
            if isinstance(locator, str):
                validation.require(bool(ENV_REFERENCE.fullmatch(locator)), f"{prefix}.transport: locator must be an environment-variable reference")

        authentication = server.get("authentication")
        validation.require(isinstance(authentication, dict), f"{prefix}.authentication: must be an object")
        if isinstance(authentication, dict):
            auth_type = authentication.get("type")
            env_names = authentication.get("credential_env")
            validation.require(auth_type in {"none", "api_key", "oauth2", "bearer", "mtls"}, f"{prefix}.authentication.type: invalid value")
            validation.require(isinstance(env_names, list), f"{prefix}.authentication.credential_env: must be an array")
            if isinstance(env_names, list):
                validation.require(all(isinstance(name, str) and ENV_NAME.fullmatch(name) for name in env_names), f"{prefix}.authentication.credential_env: invalid variable name")
                validation.require(auth_type == "none" or bool(env_names), f"{prefix}.authentication: credential variable required")

        health = server.get("health_check")
        validation.require(isinstance(health, dict), f"{prefix}.health_check: must be an object")
        if isinstance(health, dict):
            validation.require(health.get("type") in {"none", "process", "http"}, f"{prefix}.health_check.type: invalid value")
            validation.require(isinstance(health.get("enabled"), bool), f"{prefix}.health_check.enabled: must be boolean")
            validation.require(isinstance(health.get("timeout_ms"), int) and health.get("timeout_ms", 0) > 0, f"{prefix}.health_check.timeout_ms: positive integer required")

        documentation = server.get("documentation")
        safe_documentation = isinstance(documentation, str) and not Path(documentation).is_absolute() and ".." not in Path(documentation).parts
        validation.require(safe_documentation and (ROOT / documentation).is_file(), f"{prefix}.documentation: safe repository file does not exist")
        if server.get("enabled") and server.get("status") in {"DRAFT", "DISABLED"}:
            validation.errors.append(f"{prefix}: enabled server cannot have status {server.get('status')}")
    return ids


def validate_clients(data: Any, server_ids: set[str], validation: Validation) -> set[str]:
    validation.require(isinstance(data, dict) and isinstance(data.get("clients"), list), "clients: root must contain clients array")
    if not isinstance(data, dict) or not isinstance(data.get("clients"), list):
        return set()
    validation.require(data.get("schema_version") == "1.0.0", "clients: schema_version must be 1.0.0")
    validation.require(set(data.keys()) == {"schema_version", "clients"}, "clients: unexpected or missing top-level fields")
    ids: set[str] = set()
    for index, client in enumerate(data["clients"]):
        prefix = f"clients[{index}]"
        validation.require(isinstance(client, dict), f"{prefix}: must be an object")
        if not isinstance(client, dict):
            continue
        missing = CLIENT_REQUIRED - client.keys()
        validation.require(not missing, f"{prefix}: missing fields {sorted(missing)}")
        validation.require(set(client.keys()) == CLIENT_REQUIRED, f"{prefix}: unexpected fields present")
        client_id = client.get("id")
        validation.require(isinstance(client_id, str) and client_id.startswith("CLIENT-"), f"{prefix}.id: invalid client ID")
        validation.require(client_id not in ids, f"{prefix}.id: duplicate {client_id}")
        if isinstance(client_id, str):
            ids.add(client_id)
        allowed_servers = client.get("server_allowlist", [])
        validation.require(isinstance(allowed_servers, list) and set(allowed_servers) <= server_ids, f"{prefix}.server_allowlist: unknown server")
        risk_classes = client.get("allowed_risk_classes", [])
        validation.require(isinstance(risk_classes, list) and bool(risk_classes) and set(risk_classes) <= RISK_CLASSES, f"{prefix}.allowed_risk_classes: invalid value")
        environments = client.get("environments", [])
        validation.require(isinstance(environments, list) and bool(environments) and set(environments) <= ENVIRONMENTS, f"{prefix}.environments: invalid value")
        documentation = client.get("documentation")
        safe_documentation = isinstance(documentation, str) and not Path(documentation).is_absolute() and ".." not in Path(documentation).parts
        validation.require(safe_documentation and (ROOT / documentation).is_file(), f"{prefix}.documentation: safe repository file does not exist")
        if "RESTRICTED" in risk_classes:
            validation.errors.append(f"{prefix}: RESTRICTED cannot be granted in a client profile")
    return ids


def validate_audit_example(data: Any, server_ids: set[str], client_ids: set[str], validation: Validation) -> None:
    validation.require(isinstance(data, dict), "audit example: root must be an object")
    if not isinstance(data, dict):
        return
    missing = AUDIT_REQUIRED - data.keys()
    validation.require(not missing, f"audit example: missing fields {sorted(missing)}")
    validation.require(set(data.keys()) == AUDIT_REQUIRED, "audit example: unexpected fields present")
    validate_iso_timestamp(data.get("timestamp"), "audit.timestamp", validation)
    validation.require(data.get("client") in client_ids, "audit.client: unknown client")
    validation.require(data.get("server") in server_ids, "audit.server: unknown server")
    validation.require(data.get("environment") in ENVIRONMENTS, "audit.environment: invalid value")
    validation.require(data.get("risk_class") in RISK_CLASSES, "audit.risk_class: invalid value")
    validation.require(data.get("approval_status") in APPROVAL_STATUSES, "audit.approval_status: invalid value")
    validation.require(data.get("result") in RESULTS, "audit.result: invalid value")
    validation.require(isinstance(data.get("approval_required"), bool), "audit.approval_required: must be boolean")
    if data.get("approval_required"):
        validation.require(data.get("approval_status") != "NOT_REQUIRED", "audit.approval_status: inconsistent with approval_required")


def validate_environment_configs(validation: Validation) -> None:
    for environment in sorted(ENVIRONMENTS):
        relative = f"configs/{environment}/mcp-core.json"
        config = load_json(relative, validation)
        if not isinstance(config, dict):
            continue
        validation.require(config.get("environment") == environment, f"{relative}: environment mismatch")
        for field in ("writes_enabled", "external_side_effects_enabled", "founder_approval_required", "health_checks_enabled", "audit_log_enabled"):
            validation.require(isinstance(config.get(field), bool), f"{relative}.{field}: must be boolean")
        if environment == "production":
            validation.require(config.get("writes_enabled") is False, f"{relative}: production writes must default false")
            validation.require(config.get("external_side_effects_enabled") is False, f"{relative}: production external side effects must default false")
            validation.require(config.get("founder_approval_required") is True, f"{relative}: Founder approval must default true")


def scan_for_secrets(validation: Validation) -> None:
    ignored_parts = {".git", "node_modules", ".venv", "venv", "__pycache__"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in ignored_parts for part in path.parts):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                validation.errors.append(f"secret scan: possible {label} in {path.relative_to(ROOT)}")


def resolve_env_reference(value: str) -> str | None:
    match = re.fullmatch(r"\$\{([A-Z][A-Z0-9_]*)\}", value)
    return os.environ.get(match.group(1)) if match else value


def runtime_health(server: dict[str, Any]) -> tuple[str, str | None]:
    if not server["enabled"]:
        return "DISABLED", None
    check = server["health_check"]
    if not check["enabled"]:
        return "READY", "runtime check not configured"
    timeout = check["timeout_ms"] / 1000
    try:
        if check["type"] == "http":
            endpoint = resolve_env_reference(server["transport"]["endpoint"])
            if not endpoint:
                return "DEGRADED", "endpoint environment variable is unset"
            url = endpoint.rstrip("/") + check.get("path", "")
            with urllib.request.urlopen(url, timeout=timeout) as response:
                if 200 <= response.status < 400:
                    return "READY", None
                return "DEGRADED", f"health endpoint returned HTTP {response.status}"
        if check["type"] == "process":
            command = resolve_env_reference(server["transport"]["command"])
            if not command:
                return "DEGRADED", "command environment variable is unset"
            args = shlex.split(command) + server["transport"].get("args", [])
            completed = subprocess.run(args, capture_output=True, timeout=timeout, check=False)
            return ("READY", None) if completed.returncode == 0 else ("DEGRADED", f"process exited {completed.returncode}")
        return "READY", None
    except (OSError, subprocess.TimeoutExpired, urllib.error.URLError) as exc:
        return "DEGRADED", str(exc)


def build_readiness(registry: dict[str, Any], check_runtime: bool) -> list[dict[str, Any]]:
    readiness = []
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    for server in registry.get("servers", []):
        if check_runtime:
            status, error = runtime_health(server)
        elif not server["enabled"]:
            status, error = "DISABLED", None
        else:
            status, error = server["status"], None
        readiness.append({
            "timestamp": timestamp,
            "server_id": server["id"],
            "enabled": server["enabled"],
            "configuration_valid": True,
            "health_status": status,
            "error": error,
        })
    return readiness


def run(check_runtime: bool = False) -> tuple[Validation, dict[str, Any]]:
    validation = Validation()
    registry = load_json("registry/mcp-registry.json", validation)
    clients = load_json("registry/clients.json", validation)
    audit = load_json("examples/audit-event.example.json", validation)
    load_json("schemas/mcp-registry.schema.json", validation)
    load_json("schemas/client-registry.schema.json", validation)
    load_json("schemas/audit-event.schema.json", validation)
    load_json("examples/codex-suri.mcp.example.json", validation)
    load_json("examples/hermes-miss-hermes.mcp.example.json", validation)
    registration_example = load_json("examples/mcp-registration.example.yaml", validation)
    version_path = ROOT / "VERSION"
    try:
        version = version_path.read_text(encoding="utf-8").strip()
        validation.require(version == "0.1.0", "VERSION: must match MCP Core 0.1.0")
    except OSError as exc:
        validation.errors.append(f"VERSION: cannot read: {exc}")
    server_ids = validate_registry(registry, validation)
    if isinstance(registration_example, dict):
        example_wrapper = {
            "schema_version": "1.0.0",
            "hub_version": "0.1.0",
            "updated_at": "2026-09-02T00:00:00Z",
            "servers": [registration_example],
        }
        validate_registry(example_wrapper, validation)
    client_ids = validate_clients(clients, server_ids, validation)
    validate_audit_example(audit, server_ids, client_ids, validation)
    validate_environment_configs(validation)
    scan_for_secrets(validation)
    readiness = build_readiness(registry, check_runtime) if isinstance(registry, dict) and not validation.errors else []
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "hub_version": registry.get("hub_version") if isinstance(registry, dict) else None,
        "validation": "PASS" if not validation.errors else "FAIL",
        "errors": validation.errors,
        "warnings": validation.warnings,
        "readiness": readiness,
    }
    return validation, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-runtime", action="store_true", help="run opt-in endpoint/process health checks for enabled servers")
    parser.add_argument("--json", action="store_true", help="emit the report as JSON")
    args = parser.parse_args()
    validation, report = run(check_runtime=args.check_runtime)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"MCP Core v{report['hub_version']} validation: {report['validation']}")
        print(f"Servers checked: {len(report['readiness'])}")
        for item in report["readiness"]:
            suffix = f" ({item['error']})" if item["error"] else ""
            print(f"- {item['server_id']}: {item['health_status']}{suffix}")
        for error in validation.errors:
            print(f"ERROR: {error}")
        for warning in validation.warnings:
            print(f"WARNING: {warning}")
    return 0 if not validation.errors else 1


if __name__ == "__main__":
    sys.exit(main())
