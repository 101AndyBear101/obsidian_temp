"""Executable checks for standalone vault validation scripts."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
VAULT_ROOT = SCRIPTS_DIR.parents[1]


class ValidationScriptTests(unittest.TestCase):
    def test_each_validation_script_exits_successfully(self):
        scripts = sorted(
            path
            for path in SCRIPTS_DIR.glob("*_validation.py")
            if path.name != "master_validation.py"
        )
        self.assertTrue(scripts, "expected at least one validation script")

        for script in scripts:
            with self.subTest(script=script.name):
                result = subprocess.run(
                    [sys.executable, str(script)],
                    cwd=VAULT_ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=f"{script.name} failed:\n{result.stdout}{result.stderr}",
                )
