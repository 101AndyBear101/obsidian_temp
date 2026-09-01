"""Regression tests for daily-journal handling in orphan validators."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]


def load_validator(name: str):
    path = SCRIPTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DailyJournalOrphanRegressionTests(unittest.TestCase):
    def test_daily_journals_are_ignored_but_regular_orphans_are_reported(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            daily_note = vault / "journals" / "days" / "2026-08-28.md"
            regular_note = vault / "notes" / "unlinked-note.md"
            daily_note.parent.mkdir(parents=True)
            regular_note.parent.mkdir(parents=True)
            daily_note.write_text("# Daily journal\n", encoding="utf-8")
            regular_note.write_text("# Unlinked note\n", encoding="utf-8")

            for name in ("inbound_validation", "orphan_validation"):
                with self.subTest(validator=name):
                    validator = load_validator(name)
                    validator.VAULT_ROOT = str(vault)
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        with self.assertRaises(SystemExit) as exit_context:
                            validator.main()

                    self.assertEqual(exit_context.exception.code, 1)
                    self.assertIn("ORPHAN: notes/unlinked-note.md", output.getvalue())
                    self.assertNotIn("journals/days/2026-08-28.md", output.getvalue())
