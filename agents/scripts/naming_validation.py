#!/usr/bin/env python3
# agents/scripts/naming_validation.py
"""
Scan files and folders for lowercase-kebab-case compliance.

Skips reserved names (AGENTS.md, README.md, INDEX.md, SKILL.md) and
hidden directories (.git, .obsidian, node_modules).

Usage: python agents/scripts/naming_validation.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}
RESERVED_NAMES = {"AGENTS.md", "README.md", "INDEX.md", "SKILL.md"}
ALLOWED_EXEMPTIONS = {"makefile", "Dockerfile", "LICENSE", ".env.example", ".gitignore"}

KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$", re.IGNORECASE)


def main():
    errors = 0

    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for name in dirs + files:
            path = os.path.join(root, name)
            rel = os.path.relpath(path, VAULT_ROOT).replace("\\", "/")

            if name in RESERVED_NAMES or name.lower() in ALLOWED_EXEMPTIONS:
                continue

            if not KEBAB_RE.match(name):
                base, ext = os.path.splitext(name)
                if not KEBAB_RE.match(base) and ext.lower() == ext:
                    print(f"NAMING: {rel}")
                    errors += 1

    if errors == 0:
        print("All names follow lowercase-kebab-case.")
    else:
        print(f"\nFound {errors} naming issue(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()