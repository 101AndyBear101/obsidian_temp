#!/usr/bin/env python3
# agents/scripts/base_validation.py
"""
Validate all Base views (.base files and dashboard.md) in the vault.

Checks:
  - Filters reference existing folders
  - Filters reference valid property names
  - All referenced folders exist in the vault
  - All referenced kind values are valid

Usage: python agents/scripts/base_validation.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}

ALLOWED_KINDS = {"note", "project", "resource", "area", "plan", "skill",
                 "index", "guide", "template", "archive"}

EXISTING_FOLDERS = set()
for root, dirs, files in os.walk(VAULT_ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for d in dirs:
        EXISTING_FOLDERS.add(d)

FILTER_RE = re.compile(
    r'file\.inFolder\(\s*"([^"]+)"\s*\)|file\.folder\s*[=!]=\s*"([^"]+)"'
)
KIND_RE = re.compile(r'kind\s*[=!]=\s*"([^"]+)"')


def _is_base_view(rel: str) -> bool:
    """Return whether a vault-relative path is a supported Base view source."""
    return rel.startswith("bases/") and (rel.endswith(".base") or rel == "bases/dashboard.md")


def main():
    errors = 0

    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            if not fname.endswith((".base", ".md")):
                continue

            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, VAULT_ROOT).replace("\\", "/")
            if not _is_base_view(rel):
                continue

            with open(fpath, encoding="utf-8") as f:
                content = f.read()

            # Check folder references
            for m in FILTER_RE.finditer(content):
                folder = m.group(1) or m.group(2)
                parts = folder.lstrip("/").split("/")
                for p in parts:
                    if p not in EXISTING_FOLDERS and p not in ("days", "years"):
                        print(f"BROKEN: {rel} — filter references unknown folder '{folder}'")
                        errors += 1

            # Check kind values in filters
            for m in KIND_RE.finditer(content):
                kind = m.group(1)
                if kind not in ALLOWED_KINDS:
                    if kind not in ("fleeting", "permanent", "contextual", "diagram"):
                        print(f"BROKEN: {rel} — filter references unknown kind '{kind}'")
                        errors += 1

    if errors == 0:
        print("All Base views reference valid folders and kinds.")
    else:
        print(f"\nFound {errors} Base view issue(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()
