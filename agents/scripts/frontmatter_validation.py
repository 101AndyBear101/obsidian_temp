#!/usr/bin/env python3
# agents/scripts/frontmatter_validation.py
"""
Validate all .md files against the CONVENTIONS metadata schema.

Reports:
  - Missing required fields per kind
  - Invalid kind/status/type values
  - Relationship values using .md extension (should be bare filenames)
  - Invalid ISO date format in 'created'

Usage: python agents/scripts/frontmatter_validation.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}

ALLOWED_KINDS = {"note", "project", "resource", "area", "plan", "skill",
                 "index", "guide", "template", "archive"}
ALLOWED_STATUS = {"active", "paused", "complete", "archive"}
ALLOWED_TYPES = {"permanent", "fleeting", "contextual", "diagram"}

REQUIRED_BY_KIND = {
    "note":     ["kind", "status", "created"],
    "project":  ["kind", "status", "created", "area"],
    "resource": ["kind", "status", "created"],
    "area":     ["kind", "status", "created"],
    "plan":     ["kind", "status", "created"],
    "skill":    ["kind", "status", "created"],
    "guide":    ["kind", "status", "created"],
    "index":    ["kind", "status", "created"],
    "template": ["kind", "status", "created"],
    "archive":  ["kind", "status", "created"],
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter fields into a dict."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = 1
    while end < len(lines) and lines[end].strip() != "---":
        end += 1
    fm = {}
    for line in lines[1:end]:
        m = re.match(r"^(\w+(?:-\w+)*)\s*:\s*(.*)", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def _has_value(fm: dict, prop: str) -> bool:
    """Check if a property has a real value (not empty and not empty list)."""
    val = fm.get(prop, "")
    if not val:
        return False
    if val.strip() in ("[]", "{}", ""):
        return False
    return True


def _is_skill_file(fname: str, fm: dict) -> bool:
    """Check if this is a skill file using name: frontmatter instead of kind:."""
    return fname == "SKILL.md" and fm.get("name", "") and not fm.get("kind", "")


def main():
    errors = 0

    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, VAULT_ROOT).replace("\\", "/")

            with open(fpath, encoding="utf-8") as f:
                content = f.read()

            if rel.startswith("templates/base/"):
                # Unrendered Templater source is checked by template_validation.py.
                continue

            if not content.startswith("---"):
                continue

            fm = _parse_frontmatter(content)
            if not fm:
                continue

            # Skip SKILL.md files that use name: frontmatter
            if _is_skill_file(fname, fm):
                continue

            kind = fm.get("kind", "")
            status = fm.get("status", "")
            ntype = fm.get("type", "")
            created = fm.get("created", "")

            # --- kind ---
            if not kind:
                print(f"MISSING: {rel} — no 'kind' property")
                errors += 1
            elif kind not in ALLOWED_KINDS:
                print(f"INVALID: {rel} — unknown kind '{kind}' (allowed: {sorted(ALLOWED_KINDS)})")
                errors += 1
            else:
                # --- required per kind (skip templates — they use placeholders) ---
                if "templates/" not in rel and kind in REQUIRED_BY_KIND:
                    for prop in REQUIRED_BY_KIND[kind]:
                        if not _has_value(fm, prop):
                            print(f"MISSING: {rel} — '{prop}' required for kind '{kind}'")
                            errors += 1

            # --- status ---
            if not status:
                print(f"MISSING: {rel} — no 'status' property")
                errors += 1
            elif status not in ALLOWED_STATUS:
                print(f"INVALID: {rel} — unknown status '{status}' (allowed: {sorted(ALLOWED_STATUS)})")
                errors += 1

            # --- type ---
            if ntype and ntype not in ALLOWED_TYPES:
                print(f"INVALID: {rel} — unknown type '{ntype}' (allowed: {sorted(ALLOWED_TYPES)})")
                errors += 1

            # --- created ---
            if not created:
                print(f"MISSING: {rel} — no 'created' property")
                errors += 1
            elif not DATE_RE.match(created):
                print(f"INVALID: {rel} — 'created' not ISO date: '{created}'")
                errors += 1

            # --- relationship values: check no .md extension ---
            for rel_prop in ("area", "project", "resource"):
                raw = fm.get(rel_prop, "")
                if ".md" in raw:
                    print(f"INVALID: {rel} — '{rel_prop}' contains .md extension (use bare filename)")
                    errors += 1

    if errors == 0:
        print("All frontmatter checks passed.")
    else:
        print(f"\nFound {errors} frontmatter issue(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()