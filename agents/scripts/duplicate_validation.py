#!/usr/bin/env python3
# agents/scripts/duplicate_validation.py
"""
Find files with suspiciously similar filenames that may be duplicates.

Usage: python agents/scripts/duplicate_validation.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}
SKIP_NAMES = {"AGENTS.md", "README.md", "INDEX.md", "SKILL.md"}

STOP_WORDS = {
    "diagram", "template", "md", "guidance", "reference",
    "standard", "overview", "chart", "data", "model", "note",
    "workflow", "homelab", "wiki", "entity", "relationship",
    "class", "sequence", "state", "gantt", "plan", "base",
    "service", "math",
}
SIMILARITY_THRESHOLD = 0.75


def _name_parts(name: str) -> set:
    stem = os.path.splitext(name)[0].lower()
    return set(stem.split("-")) - STOP_WORDS


def _is_suspicious_pair(parts_a: set, parts_b: set) -> bool:
    """Return whether meaningful filename terms substantially overlap."""
    union = parts_a | parts_b
    return bool(union) and len(parts_a & parts_b) / len(union) > SIMILARITY_THRESHOLD


def _regression_check() -> list[str]:
    """Keep related plan names from regressing into duplicate false positives."""
    errors = []
    if _is_suspicious_pair(
        _name_parts("vault-quality-improvement-plan.md"),
        _name_parts("vault-quality-improvement-orchestration-plan.md"),
    ):
        errors.append("INTERNAL: related-plan filename regression case was flagged")
    if not _is_suspicious_pair(
        _name_parts("backup-verification.md"),
        _name_parts("homelab-backup-verification.md"),
    ):
        errors.append("INTERNAL: normalized duplicate filename regression case was missed")
    return errors


def main():
    regression_errors = _regression_check()
    if regression_errors:
        print("\n".join(regression_errors))
        sys.exit(1)

    words_to_files = {}
    parts_by_name = {}

    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            if not fname.endswith(".md"):
                continue
            if fname in SKIP_NAMES:
                continue
            rel = os.path.relpath(os.path.join(root, fname), VAULT_ROOT).replace("\\", "/")

            parts = _name_parts(fname)
            if not parts:
                continue  # all words are stop words
            for word in parts:
                if word not in words_to_files:
                    words_to_files[word] = []
                words_to_files[word].append(rel)
            parts_by_name[rel] = parts

    errors = 0
    seen_pairs = set()

    for word, rels in sorted(words_to_files.items(), key=lambda x: -len(x[1])):
        if len(rels) < 2:
            continue
        for i, a in enumerate(rels):
            for b in rels[i + 1:]:
                pair = tuple(sorted([a, b]))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)

                parts_a = parts_by_name.get(a, set())
                parts_b = parts_by_name.get(b, set())
                overlap = parts_a & parts_b
                if _is_suspicious_pair(parts_a, parts_b):
                    print(f"SIMILAR: {a} <-> {b}")
                    print(f"  Common: {sorted(overlap)}")
                    errors += 1

    if errors == 0:
        print("No suspicious filename duplicates found.")
    else:
        print(f"\nFound {errors} potentially duplicate file pair(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()
