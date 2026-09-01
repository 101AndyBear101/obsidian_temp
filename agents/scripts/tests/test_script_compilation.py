"""Compilation checks for Python scripts directly under ``agents/scripts``."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]


class ScriptCompilationTests(unittest.TestCase):
    def test_all_script_files_compile(self):
        scripts = sorted(SCRIPTS_DIR.glob("*.py"))
        self.assertTrue(scripts, "expected Python scripts")

        for script in scripts:
            with self.subTest(script=script.name):
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(script)],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=f"{script.name} did not compile:\n{result.stderr}",
                )
