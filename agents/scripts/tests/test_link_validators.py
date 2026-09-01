"""Unit tests for link and attachment validation helpers."""

from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class LinkValidatorTests(unittest.TestCase):
    def test_wikilink_and_index_targets_split_aliases_and_headings(self):
        wikilinks = load("wikilink_validation")
        indexes = load("index_validation")
        self.assertEqual(wikilinks._split_target("notes/example#Purpose|Read"), ("notes/example", "Purpose"))
        self.assertEqual(indexes._split_target("notes/example#Purpose|Read"), ("notes/example", "Purpose"))

    def test_attachment_resolver_finds_path_qualified_embed(self):
        validator = load("attachment_validation")
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            attachment = vault / "files" / "sample.pdf"
            attachment.parent.mkdir()
            attachment.write_text("pdf", encoding="utf-8")
            validator.VAULT_ROOT = str(vault)
            self.assertEqual(
                os.path.normcase(validator._resolve_embed_path("files/sample.pdf")),
                os.path.normcase(str(attachment)),
            )
