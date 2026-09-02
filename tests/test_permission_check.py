import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "check_permission.py"
SPEC = importlib.util.spec_from_file_location("check_permission", MODULE_PATH)
permission = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(permission)


class PermissionCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.servers = json.loads((ROOT / "registry/mcp-registry.json").read_text())["servers"]
        cls.clients = json.loads((ROOT / "registry/clients.json").read_text())["clients"]

    def get_client(self, client_id):
        return copy.deepcopy(next(item for item in self.clients if item["id"] == client_id))

    def get_server(self, server_id):
        return copy.deepcopy(next(item for item in self.servers if item["id"] == server_id))

    def test_committed_servers_are_blocked_while_disabled(self):
        decision = permission.evaluate_permission(
            self.get_client("CLIENT-CODEX-SURI"),
            self.get_server("MCP-RES-001"),
            "web.search",
            "development",
        )
        self.assertEqual("BLOCK", decision["decision"])
        self.assertEqual("server disabled", decision["reason"])

    def test_ready_read_only_request_can_pass(self):
        server = self.get_server("MCP-RES-001")
        server.update(enabled=True, status="READY")
        decision = permission.evaluate_permission(
            self.get_client("CLIENT-CODEX-SURI"), server, "web.search", "development"
        )
        self.assertEqual("ALLOW", decision["decision"])

    def test_approval_required_request_is_blocked_without_approval(self):
        server = self.get_server("MCP-DEV-001")
        server.update(enabled=True, status="READY")
        decision = permission.evaluate_permission(
            self.get_client("CLIENT-CODEX-SURI"), server, "pull_request.draft", "development"
        )
        self.assertEqual("BLOCK", decision["decision"])
        self.assertEqual("Founder approval not recorded", decision["reason"])

    def test_restricted_is_never_allowed(self):
        client = self.get_client("CLIENT-CODEX-SURI")
        client["allowed_risk_classes"].append("RESTRICTED")
        server = self.get_server("MCP-DEV-001")
        server.update(enabled=True, status="READY", risk_class="RESTRICTED")
        decision = permission.evaluate_permission(
            client, server, "pull_request.draft", "development", "APPROVED"
        )
        self.assertEqual("BLOCK", decision["decision"])


if __name__ == "__main__":
    unittest.main()
