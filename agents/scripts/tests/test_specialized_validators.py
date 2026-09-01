"""Unit tests for specialized validator rules and script registries."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SpecializedValidatorTests(unittest.TestCase):
    def test_duplicate_similarity_distinguishes_related_and_duplicate_names(self):
        validator = load("duplicate_validation")
        self.assertFalse(validator._is_suspicious_pair({"vault", "quality", "improvement"}, {"vault", "quality", "improvement", "orchestration"}))
        self.assertTrue(validator._is_suspicious_pair({"backup", "verification"}, {"backup", "verification"}))

    def test_template_fence_validation_rejects_unmatched_closer(self):
        validator = load("template_validation")
        errors = validator.diagram_fence_errors("```\n", "mermaid", "fixture.md")
        self.assertTrue(any("unmatched closing Markdown fence" in error for error in errors))

    def test_base_filter_and_skill_index_patterns_match_supported_syntax(self):
        base_validator = load("base_validation")
        skill_validator = load("skill_validation")
        self.assertEqual(base_validator.FILTER_RE.search('file.inFolder("notes")').group(1), "notes")
        self.assertEqual(base_validator.FILTER_RE.search('file.folder == "journals/days"').group(2), "journals/days")
        self.assertEqual(base_validator.KIND_RE.search('kind == "note"').group(1), "note")
        self.assertTrue(base_validator._is_base_view("bases/dashboard.md"))
        self.assertFalse(base_validator._is_base_view("agents/skills/obsidian-bases/SKILL.md"))
        self.assertEqual(skill_validator.re.match(r"\|\s*`([a-z][a-z0-9-]+)`\s*\|", "| `example-skill` | link |").group(1), "example-skill")
