#!/usr/bin/env python3
# agents/scripts/relationship_validation.py
"""
Validate that all relationship metadata values (area, project, resource)
point to existing .md files in the vault.

Detects:
  - area/project/resource values referencing non-existent notes
  - Relationship properties with values that don't match any file

Usage: python agents/scripts/relationship_validation.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}


def _build_filename_index() -> dict:
    """Build {lowercase_name: relative_path} for all .md files."""
    index = {}
    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if fname.endswith(".md"):
                name = fname[:-3].lower()
                rel = os.path.relpath(os.path.join(root, fname), VAULT_ROOT).replace("\\", "/")
                index[name] = rel
    return index


def _parse_relationship_values(fm_text: str, prop: str) -> list:
    """Extract values from a frontmatter property (scalar or list)."""
    values = []
    lines = fm_text.splitlines()
    in_prop = False
    for line in lines:
        m = re.match(rf"^{prop}\s*:\s*(.*)", line)
        if m:
            raw = m.group(1).strip()
            if raw and raw[0] != "-":
                values.append(raw.split("#")[0].strip())
                continue
            in_prop = True
            if raw.startswith("- "):
                values.append(raw[2:].strip())
        elif in_prop and line.strip().startswith("- "):
            values.append(line.strip()[2:].strip())
        elif in_prop and not line.strip().startswith("- "):
            in_prop = False
    cleaned = []
    for v in values:
        v = v.strip().strip("'\"").strip(",")
        if v and v not in ("[]", "{}", ""):
            v = v.split("#")[0].split(" ")[0].strip()
            if v:
                cleaned.append(v.lower())
    return cleaned


def main():
    errors = 0
    file_index = _build_filename_index()
    rel_props = {"area", "project", "resource"}

    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, VAULT_ROOT).replace("\\", "/")

            if "templates/" in rel:
                continue

            with open(fpath, encoding="utf-8") as f:
                content = f.read()

            if not content.startswith("---"):
                continue

            lines = content.splitlines()
            end = 1
            while end < len(lines) and lines[end].strip() != "---":
                end += 1
            fm_text = "\n".join(lines[1:end])

            for prop in rel_props:
                values = _parse_relationship_values(fm_text, prop)
                for val in values:
                    if val not in file_index:
                        print(f"BROKEN: {rel} — '{prop}: {val}' does not match any .md file")
                        errors += 1

    if errors == 0:
        print("All relationship metadata values resolve to existing files.")
    else:
        print(f"\nFound {errors} broken relationship value(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()