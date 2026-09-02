import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_registry.py"
SPEC = importlib.util.spec_from_file_location("validate_registry", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)


class RegistryValidationTests(unittest.TestCase):
    def test_repository_contract_is_valid(self):
        validation, report = validator.run(check_runtime=False)
        self.assertEqual([], validation.errors)
        self.assertEqual("PASS", report["validation"])

    def test_all_registered_servers_are_safe_by_default(self):
        validation = validator.Validation()
        registry = validator.load_json("registry/mcp-registry.json", validation)
        self.assertEqual([], validation.errors)
        self.assertTrue(all(server["enabled"] is False for server in registry["servers"]))

    def test_production_defaults_are_conservative(self):
        validation = validator.Validation()
        config = validator.load_json("configs/production/mcp-core.json", validation)
        self.assertEqual([], validation.errors)
        self.assertFalse(config["writes_enabled"])
        self.assertFalse(config["external_side_effects_enabled"])
        self.assertTrue(config["founder_approval_required"])


if __name__ == "__main__":
    unittest.main()
