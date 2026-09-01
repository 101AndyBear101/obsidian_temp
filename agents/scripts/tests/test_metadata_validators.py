"""Unit tests for metadata-oriented validation helpers."""

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


class MetadataValidatorTests(unittest.TestCase):
    def test_frontmatter_parser_and_empty_values(self):
        validator = load("frontmatter_validation")
        frontmatter = validator._parse_frontmatter("---\nkind: note\nresource: []\n---\n")
        self.assertEqual(frontmatter["kind"], "note")
        self.assertFalse(validator._has_value(frontmatter, "resource"))

    def test_relationship_parser_handles_scalar_and_list_values(self):
        validator = load("relationship_validation")
        self.assertEqual(
            validator._parse_relationship_values("resource:\n  - alpha\n  - beta\narea: home\n", "resource"),
            ["alpha", "beta"],
        )
        self.assertEqual(validator._parse_relationship_values("area: home\n", "area"), ["home"])

    def test_section_parser_returns_only_second_level_headings(self):
        validator = load("section_validation")
        self.assertEqual(validator._get_headings("# Title\n## Purpose\n### Detail\n## Related\n"), ["Purpose", "Related"])

    def test_tag_and_name_patterns_reject_invalid_values(self):
        tag_validator = load("tag_validation")
        naming_validator = load("naming_validation")
        self.assertIsNotNone(tag_validator.TAG_RE.match("  - vault/quality"))
        self.assertIsNone(naming_validator.KEBAB_RE.match("Invalid Name"))
        self.assertIsNotNone(naming_validator.KEBAB_RE.match("valid-file_name.md"))
