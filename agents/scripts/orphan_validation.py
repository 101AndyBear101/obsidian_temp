#!/usr/bin/env python3
# agents/scripts/orphan_validation.py
"""
Find files with no inbound wikilinks from other notes.

Helps identify unused or disconnected content. Skips reserved names and
self-contained paths, including daily journals surfaced by Base views.

Usage: python agents/scripts/orphan_validation.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}
RESERVED_NAMES = {"AGENTS.md", "README.md", "INDEX.md", "SKILL.md"}

SELF_CONTAINED_PATTERNS = (
    "journals/days/",
    "templates/",
    "plans/",
    "bases/",
    "references/",
    "mermaid_diagrams/",
    "plantuml_diagrams/",
)

LINK_TARGET_RE = re.compile(r"(?<!!)\[\[([^]]+?)(?:\|[^]]+)?\]\]")


def _basename_to_link_targets(basename: str) -> list:
    """Generate possible link target patterns for a given basename."""
    name = os.path.splitext(basename)[0]
    return [name, name + ".md"]


def main():
    # Build a set of all .md files (rel path)
    all_files = {}
    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".md"):
                rel = os.path.relpath(os.path.join(root, f), VAULT_ROOT).replace("\\", "/")
                all_files[rel] = f

    # Build a set of all referenced targets (basename only, no path)
    referenced = set()
    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".md"):
                continue
            fpath = os.path.join(root, f)
            with open(fpath, encoding="utf-8") as fh:
                for match in LINK_TARGET_RE.finditer(fh.read()):
                    target = match.group(1).split("#")[0]  # strip heading
                    referenced.add(target.lower())

    errors = 0
    for rel, fname in sorted(all_files.items()):
        # Skip reserved names
        if fname in RESERVED_NAMES:
            continue

        # Skip root files that serve as entry points
        if rel in ("README.md", "CONVENTIONS.md", "AGENTS.md"):
            continue

        # Skip self-contained paths (templates, plans, bases, references, diagrams)
        if any(p in rel for p in SELF_CONTAINED_PATTERNS):
            continue

        name = os.path.splitext(fname)[0].lower()
        if name not in referenced:
            # Also check if any path-qualified link points to it
            path_pattern = rel.lower().replace("\\", "/").removesuffix(".md")
            if path_pattern not in referenced:
                print(f"ORPHAN: {rel}")
                errors += 1

    if errors == 0:
        print("No orphans found.")
    else:
        print(f"\nFound {errors} orphan file(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()
