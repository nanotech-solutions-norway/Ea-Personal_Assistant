"""Synthetic, no-provider-access tests for GitHub staging secret wiring."""

import pathlib
import subprocess
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import github_secrets_staging_preflight as checker

STAGING = {
    "EA_STAGING_CREDENTIAL_SOURCE": "github_actions_environment",
    "EA_STAGING_DATA_SCOPE": "synthetic_only",
    "BRING_API_UID": "synthetic-account-uid",
    "BRING_API_KEY": "synthetic-key-never-used",
    "BRING_CLIENT_URL": "https://synthetic.example.invalid/mybring",
}


class GithubSecretsStagingTests(unittest.TestCase):
    def test_synthetic_configuration_passes_without_network(self):
        self.assertEqual(checker.assess(STAGING), "PASS")

    def test_secret_absent_is_fail_closed(self):
        for key in checker.REQUIRED:
            with self.subTest(key=key):
                entry = dict(STAGING)
                entry.pop(key)
                self.assertEqual(
                    checker.assess(entry),
                    "BLOCKED_MISSING_GITHUB_ENVIRONMENT_CONFIG",
                )

    def test_forbidden_production_flags(self):
        for key in checker.FORBIDDEN_TRUE:
            with self.subTest(key=key):
                entry = dict(STAGING, **{key: "YES"})
                self.assertEqual(
                    checker.assess(entry),
                    "BLOCKED_LIVE_PROVIDER_OR_PRODUCTION_FLAG",
                )

    def test_never_allow_other_credential_sources(self):
        for value in ("key_vault", "github_repo_secret", "", "user_json"):
            entry = dict(STAGING, EA_STAGING_CREDENTIAL_SOURCE=value)
            self.assertEqual(checker.assess(entry), "BLOCKED_WRONG_CREDENTIAL_SOURCE")

    def test_no_non_synthetic_scope(self):
        for value in ("production", "real_shipments", "", "synthetic_only "):
            entry = dict(STAGING, EA_STAGING_DATA_SCOPE=value)
            self.assertEqual(checker.assess(entry), "BLOCKED_NON_SYNTHETIC_SCOPE")

    def test_reject_url_injection_and_creds(self):
        invalid = (
            "http://synthetic.example.invalid",
            "https://user:pass@synthetic.example.invalid",
            "https://synthetic.example.invalid/?k=secret",
            "https://synthetic.example.invalid/#fragment",
            "https://synthetic.example.invalid:444/path",
            "https://synthetic.example.invalid/" + "\n" + "leak",
            "https://synthetic.example.invalid:bogus",
        )
        for value in invalid:
            with self.subTest(url=value):
                entry = dict(STAGING, BRING_CLIENT_URL=value)
                self.assertEqual(checker.assess(entry), "BLOCKED_INVALID_CLIENT_URL")

    def test_reject_unprintable_secrets(self):
        for key in ("BRING_API_UID", "BRING_API_KEY"):
            for value in ("a\nb", "\x00secret", " ", "x" * 1025):
                if value == " ":
                    # A space is printable; but still not an acceptable
                    # populated credential. Test dangerous control chars here.
                    continue
                with self.subTest(key=key, length=len(value)):
                    entry = dict(STAGING, **{key: value})
                    self.assertEqual(checker.assess(entry), "BLOCKED_INVALID_SECRET_FORMAT")

    def test_sanitized_result_does_not_contain_secrets(self):
        sensitive = "SUPERSECRET-SYNTHETIC-DO-NOT-PRINT"
        bad = dict(STAGING, BRING_API_KEY=sensitive + "\n")
        result = checker.assess(bad)
        self.assertNotIn(sensitive, result)
        self.assertNotIn(STAGING["BRING_CLIENT_URL"], result)

    def test_main_prints_only_fixed_markers(self):
        path = pathlib.Path(checker.__file__)
        result = subprocess.run(
            [sys.executable, str(path)],
            env=STAGING,
            capture_output=True, text=True, check=False,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("EA_GITHUB_SECRETS_STAGING_PREFLIGHT=PASS", result.stdout)
        for sensitive in (STAGING["BRING_API_UID"], STAGING["BRING_API_KEY"],
                          STAGING["BRING_CLIENT_URL"]):
            self.assertNotIn(sensitive, result.stdout)
            self.assertNotIn(sensitive, result.stderr)


if __name__ == "__main__":
    unittest.main()
