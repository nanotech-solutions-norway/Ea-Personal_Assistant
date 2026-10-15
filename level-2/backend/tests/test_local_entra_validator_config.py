"""Offline tests for publicly committed local Entra sign-in helper.

No real tenant IDs, tokens, Microsoft sign-in, provider calls or secrets.
"""

import contextlib
import io
import os
import pathlib
import runpy
import unittest
from unittest.mock import patch

SCRIPT = pathlib.Path(__file__).resolve().parents[3] / "verify_ea_entra.py"
A = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
B = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
C = "cccccccc-cccc-4ccc-8ccc-cccccccccccc"


class LocalEntraValidatorConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.methods = runpy.run_path(str(SCRIPT))

    def test_valid_synthetic_config(self):
        config = {
            "EA_ENTRA_TENANT_ID": A,
            "EA_API_CLIENT_ID": B,
            "EA_AUTHORIZED_CLIENT_ID": C,
        }
        self.assertEqual(self.methods["read_configuration"](config), (A, B, C))

    def test_missing_configuration_fails_closed(self):
        with self.assertRaises(ValueError):
            self.methods["read_configuration"]({})

    def test_invalid_identifier_fails_closed(self):
        with self.assertRaises(ValueError):
            self.methods["read_configuration"]({
                "EA_ENTRA_TENANT_ID": "example.com/not-a-tenant",
                "EA_API_CLIENT_ID": B,
                "EA_AUTHORIZED_CLIENT_ID": C,
            })

    def test_no_interactive_login_attempt_with_missing_configuration(self):
        with patch.dict(os.environ, {}, clear=True):
            result = io.StringIO()
            with contextlib.redirect_stdout(result):
                exit_code = self.methods["main"]()
        self.assertEqual(exit_code, 2)
        self.assertEqual(
            result.getvalue().strip(),
            "EA_ENTRA_VALIDATION=BLOCKED_INVALID_CONFIG",
        )

    def test_no_hardcoded_organization_config_in_source(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn('TENANT_ID = "', source)
        self.assertNotIn('API_CLIENT_ID = "', source)
        self.assertNotIn('DESKTOP_CLIENT_ID = "', source)
        self.assertIn('if __name__ == "__main__"', source)


if __name__ == "__main__":
    unittest.main()
