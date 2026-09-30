import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from preflight import check, REQUIRED


class PreflightTests(unittest.TestCase):
    def test_missing_dependencies_block_readiness(self):
        result = check({})
        self.assertFalse(result.ready)
        self.assertEqual(set(result.missing), set(REQUIRED))

    def test_level2a_safe_config_can_be_ready(self):
        env = {key: "configured" for key in REQUIRED}
        env.update({
            "EA_LEVEL_2B_ENABLED": "false",
            "EA_EXTERNAL_SEND_ENABLED": "false",
            "EA_EXTERNAL_CALENDAR_ENABLED": "false",
        })
        result = check(env)
        self.assertTrue(result.ready)
        self.assertEqual(result.unsafe_flags, ())

    def test_external_send_flag_fails_closed(self):
        env = {key: "configured" for key in REQUIRED}
        env["EA_EXTERNAL_SEND_ENABLED"] = "true"
        result = check(env)
        self.assertFalse(result.ready)
        self.assertIn("EA_EXTERNAL_SEND_ENABLED", result.unsafe_flags)


if __name__ == "__main__":
    unittest.main()
