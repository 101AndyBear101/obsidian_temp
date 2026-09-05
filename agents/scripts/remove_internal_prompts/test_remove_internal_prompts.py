"""Tests for removing agent-only internal prompt fences."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def load_script():
    spec = importlib.util.spec_from_file_location(
        "remove_internal_prompts", SCRIPT_DIR / "remove_internal_prompts.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RemoveInternalPromptsTests(unittest.TestCase):
    def setUp(self):
        self.script = load_script()

    def test_removes_prompt_and_preserves_answer_below_it(self):
        source = """## Overview\n\n```internal_prompt\nAsk a question.\n```\nThe answer remains.\n"""

        updated, removed = self.script.remove_internal_prompts(source)

        self.assertEqual(removed, 1)
        self.assertEqual(updated, "## Overview\n\nThe answer remains.\n")

    def test_collapses_the_blank_line_left_by_a_removed_prompt(self):
        source = """## Overview\n\n```internal_prompt\nAsk a question.\n```\n\nThe answer remains.\n"""

        updated, removed = self.script.remove_internal_prompts(source)

        self.assertEqual(removed, 1)
        self.assertEqual(updated, "## Overview\n\nThe answer remains.\n")

    def test_preserves_non_prompt_fences(self):
        source = """```python\nprint(\"keep\")\n```\n"""

        updated, removed = self.script.remove_internal_prompts(source)

        self.assertEqual(removed, 0)
        self.assertEqual(updated, source)

    def test_rejects_unclosed_prompt_without_returning_partial_output(self):
        source = """```internal_prompt\nAsk a question.\n"""

        with self.assertRaisesRegex(ValueError, "Unclosed internal_prompt fence"):
            self.script.remove_internal_prompts(source)


if __name__ == "__main__":
    unittest.main()
