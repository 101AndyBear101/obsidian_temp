"""Unit tests for master validation script discovery."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent


class MasterValidationTests(unittest.TestCase):
    def test_master_discovers_every_validation_script(self):
        master_path = SCRIPTS_DIR / "master_validation.py"
        spec = importlib.util.spec_from_file_location("master_validation", master_path)
        master = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(master)

        expected = sorted(
            path.stem
            for path in SCRIPTS_DIR.glob("*_validation.py")
            if path.name != "master_validation.py"
        )
        discovered = sorted(
            path.stem
            for path in Path(master.SCRIPTS_DIR).glob("*_validation.py")
            if path.name != "master_validation.py"
        )
        self.assertEqual(discovered, expected)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(str(SCRIPTS_DIR / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
