#!/usr/bin/env python3
# agents/scripts/skill_validation.py
"""
Validate the agents/skills/ directory against its INDEX.md registry.

Checks:
  - Every skill folder has a SKILL.md file
  - Every skill folder is listed in INDEX.md
  - Every skill listed in INDEX.md has a corresponding folder
  - New/unregistered skill folders are flagged for ingestion

Usage: python agents/scripts/skill_validation.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKILLS_DIR = os.path.join(VAULT_ROOT, "agents", "skills")
INDEX_FILE = os.path.join(SKILLS_DIR, "INDEX.md")


def _registered_skills_from_index() -> set:
    """Extract skill names from the INDEX.md table entries."""
    if not os.path.exists(INDEX_FILE):
        print("MISSING: agents/skills/INDEX.md — no registry found")
        sys.exit(1)

    with open(INDEX_FILE, encoding="utf-8") as f:
        content = f.read()

    # Match skill names from table rows: | `skill-name` | link | ... |
    skills = set()
    for line in content.splitlines():
        m = re.match(r"\|\s*`([a-z][a-z0-9-]+)`\s*\|", line)
        if m:
            skills.add(m.group(1))
    return skills


def _skill_folder_names() -> set:
    """Return set of directory names under agents/skills/ (excluding files)."""
    if not os.path.exists(SKILLS_DIR):
        print("MISSING: agents/skills/ directory not found")
        sys.exit(1)

    folders = set()
    for entry in os.listdir(SKILLS_DIR):
        full = os.path.join(SKILLS_DIR, entry)
        if os.path.isdir(full):
            folders.add(entry)
    return folders


def main():
    errors = 0
    changes = {"missing_skil l": [], "unregistered": [], "orphan_entry": [], "needs_ingestion": []}

    registered = _registered_skills_from_index()
    folders = _skill_folder_names()

    print(f"Registered in INDEX.md: {len(registered)} skills")
    print(f"Folders on disk: {len(folders)} skill folders")

    # Check each folder: has SKILL.md? registered?
    for folder in sorted(folders):
        skill_path = os.path.join(SKILLS_DIR, folder, "SKILL.md")
        if not os.path.exists(os.path.join(SKILLS_DIR, folder, "SKILL.md")):
            print(f"MISSING: agents/skills/{folder}/SKILL.md — has folder but no SKILL.md")
            errors += 1
            continue

    if folder not in registered:
            print(f"UNREGISTERED: agents/skills/{folder}/ — not listed in INDEX.md (may need ingestion)")
            errors += 1
            changes["needs_ingestion"].append(folder)

    # Check each registered skill has a folder
    for skill in sorted(registered):
        if skill not in folders:
            print(f"STALE: INDEX.md lists '{skill}' but no folder exists at agents/skills/{skill}/")
            errors += 1
            changes["orphan_entry"].append(skill)

    # Summary
    if errors == 0:
        print("\nAll skills validated — registry and folders are in sync.")
    else:
        print(f"\nFound {errors} issue(s).")
        if changes["needs_ingestion"]:
            print(f"\nNew skills to ingest: {', '.join(changes['needs_ingestion'])}")
        if changes["orphan_entry"]:
            print(f"\nStale INDEX.md entries: {', '.join(changes['orphan_entry'])}")
        sys.exit(1)


if __name__ == "__main__":
    main()