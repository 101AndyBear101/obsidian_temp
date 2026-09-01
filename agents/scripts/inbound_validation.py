#!/usr/bin/env python3
# agents/scripts/inbound_validation.py
"""
Smarter orphan detection — find notes with no inbound links
from other notes, excluding known self-contained file types.

More precise than orphan_validation.py — excludes:
  - Daily journals (journals/days/), surfaced by journal Base views
  - Templates (templates/)
  - Plans (plans/)
  - Indexes (INDEX.md)
  - README files
  - Skill reference files (references/)
  - Dashboard bases (bases/)
  - Diagram templates (mermaid_diagrams/, plantuml_diagrams/)

Usage: python agents/scripts/inbound_validation.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}

SELF_CONTAINED_PATTERNS = (
    "journals/days/",
    "templates/",
    "plans/",
    "bases/",
    "references/",
    "mermaid_diagrams/",
    "plantuml_diagrams/",
)

LINK_RE = re.compile(r"(?<!!)\[\[([^]]+)\]\]")


def main():
    errors = 0

    all_files = {}
    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, fname), VAULT_ROOT).replace("\\", "/")

            skip = any(p in rel for p in SELF_CONTAINED_PATTERNS)
            if skip:
                continue
            if fname in ("AGENTS.md", "INDEX.md", "README.md", "SKILL.md"):
                continue

            all_files[rel] = fname

    referenced = set()
    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            if fname == "SKILL.md":
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, encoding="utf-8") as f:
                for match in LINK_RE.finditer(f.read()):
                    target = match.group(1).split("|")[0].split("#")[0]
                    referenced.add(target.lower())
                    if "/" in target:
                        referenced.add(target.lower())

    for rel, fname in sorted(all_files.items()):
        name = os.path.splitext(fname)[0].lower()
        path_key = rel.lower().replace("\\", "/").removesuffix(".md")
        if name not in referenced and path_key not in referenced:
            print(f"ORPHAN: {rel}")
            errors += 1

    if errors == 0:
        print("No orphan content notes found.")
    else:
        print(f"\nFound {errors} orphan content note(s) without inbound links.")
        sys.exit(1)


if __name__ == "__main__":
    main()
