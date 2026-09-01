#!/usr/bin/env python3
# agents/scripts/section_validation.py
"""
Verify permanent and contextual notes have expected sections.

Checks:
  - kind: note, type: permanent notes have ## Purpose, ## Validation, ## Related
  - kind: note, type: contextual notes have at least ## Related or embedded content
  - kind: project notes have ## Goal, ## Next Actions, ## Completion Criteria

Usage: python agents/scripts/section_validation.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}

HEADING_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)


def _parse_frontmatter(content: str) -> dict:
    lines = content.splitlines()
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


def _get_headings(content: str) -> list:
    return HEADING_RE.findall(content)


def main():
    errors = 0
    checked = 0

    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, VAULT_ROOT).replace("\\", "/")

            with open(fpath, encoding="utf-8") as f:
                content = f.read()

            if not content.startswith("---"):
                continue

            fm = _parse_frontmatter(content)
            if not fm:
                continue

            kind = fm.get("kind", "")
            ntype = fm.get("type", "")
            headings = _get_headings(content)

            checked += 1

            if kind == "note" and ntype == "permanent":
                needs = ["Purpose", "Validation", "Related"]
                for section in needs:
                    if section not in headings:
                        print(f"MISSING: {rel} — permanent note missing '## {section}' section")
                        errors += 1

            elif kind == "note" and ntype == "contextual":
                # Contextual notes should have Related or embeds
                if "Related" not in headings:
                    if "![" not in content:
                        print(f"MISSING: {rel} — contextual note missing '## Related' or embeds")
                        errors += 1

            elif kind == "project":
                needs = ["Goal", "Next Actions", "Completion Criteria"]
                for section in needs:
                    if section not in headings:
                        print(f"MISSING: {rel} — project note missing '## {section}' section")
                        errors += 1

            elif kind == "resource":
                if "Purpose" not in headings and "Key Information" not in headings:
                    print(f"MISSING: {rel} — resource note missing '## Purpose' or '## Key Information'")
                    errors += 1

            elif kind == "area":
                if "Purpose" not in headings:
                    print(f"MISSING: {rel} — area note missing '## Purpose' section")
                    errors += 1
                if "Standards" not in headings and "Active Projects" not in headings:
                    print(f"MISSING: {rel} — area note missing '## Standards' or '## Active Projects'")
                    errors += 1

    if errors == 0:
        print(f"All {checked} content notes have expected sections.")
    else:
        print(f"\nFound {errors} missing section(s) across {checked} notes.")
        sys.exit(1)


if __name__ == "__main__":
    main()