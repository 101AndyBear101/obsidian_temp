#!/usr/bin/env python3
# agents/scripts/index_validation.py
"""
Validate all INDEX.md files across the vault.

Checks:
  - Every INDEX.md has valid frontmatter (kind: index, status, created)
  - Every INDEX.md contains wikilinks
  - At least one wikilink in each INDEX.md resolves to an existing file
  - No broken wikilinks in INDEX.md files

Usage: python agents/scripts/index_validation.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}

LINK_RE = re.compile(r"(?<!!)\[\[([^]]+)\]\]")

NON_NOTE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp",
                 ".pdf", ".mp3", ".ogg", ".wav", ".base", ".canvas",
                 ".yaml", ".yml", ".json", ".xml", ".csv", ".tsv",
                 ".zip", ".tar", ".gz", ".py", ".sh"}

PLACEHOLDER_PATTERNS = r"(?:parent-resource-name|related-note|note-name|project-name|resource-name|area-name|skill-name|diagram-type-diagram|YYYY-MM-DD)"


def _split_target(raw: str) -> tuple:
    """Split [[target|alias]] into (target_name, heading_or_None)."""
    if "\\|" in raw:
        raw = raw.split("\\|")[0]
    elif "|" in raw:
        raw = raw.split("|")[0]
    heading = None
    if "#" in raw:
        raw, heading = raw.rsplit("#", 1)
    return raw, heading


def _resolve_file(target: str) -> list:
    """Return list of possible file paths for a link target."""
    base, ext = os.path.splitext(target)
    if ext:
        if ext.lower() in NON_NOTE_EXTS:
            full = os.path.join(VAULT_ROOT, target)
            return [full] if os.path.exists(full) else []
        return []

    if "/" in target:
        full = os.path.join(VAULT_ROOT, target + ".md")
        return [full] if os.path.exists(full) else []

    matches = []
    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f == target + ".md":
                matches.append(os.path.join(root, f))
    return matches


def _heading_exists(path: str, heading: str) -> bool:
    """Check if a heading exists in a markdown file."""
    with open(path, encoding="utf-8") as f:
        return bool(re.search(rf"^#+ {re.escape(heading)}$", f.read(), re.MULTILINE))


def main():
    errors = 0
    index_count = 0

    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            if fname != "INDEX.md":
                continue
            index_count += 1
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, VAULT_ROOT).replace("\\", "/")

            with open(fpath, encoding="utf-8") as f:
                content = f.read()

            # Check frontmatter
            if not content.startswith("---"):
                print(f"MISSING: {rel} — has no frontmatter")
                errors += 1
                continue

            lines = content.splitlines()
            end = 1
            while end < len(lines) and lines[end].strip() != "---":
                end += 1
            fm = {}
            for line in lines[1:end]:
                m = re.match(r"^(\w+(?:-\w+)*)\s*:\s*(.*)", line)
                if m:
                    fm[m.group(1)] = m.group(2).strip()

            kind = fm.get("kind", "")
            status = fm.get("status", "")
            created = fm.get("created", "")

            if kind != "index":
                print(f"INVALID: {rel} — kind should be 'index', got '{kind}'")
                errors += 1

            if not status:
                print(f"MISSING: {rel} — no 'status' property")
                errors += 1

            if not created:
                print(f"MISSING: {rel} — no 'created' property")
                errors += 1
            elif not re.match(r"^\d{4}-\d{2}-\d{2}$", created):
                print(f"INVALID: {rel} — 'created' not ISO date: '{created}'")
                errors += 1

            # Check wikilinks exist
            links = LINK_RE.findall(content)
            if not links:
                print(f"MISSING: {rel} — contains no wikilinks")
                errors += 1
                continue

            # Check each link resolves
            resolved = 0
            for raw in links:
                target, heading = _split_target(raw)

                if re.match(r"^(https?|mailto):", target, re.IGNORECASE):
                    continue
                if not target:
                    continue

                # Skip placeholders
                if re.search(PLACEHOLDER_PATTERNS, target, re.IGNORECASE):
                    continue

                paths = _resolve_file(target)
                if not paths:
                    print(f"BROKEN: {rel} -> [[{raw}]]")
                    errors += 1
                elif heading:
                    found = any(_heading_exists(p, heading) for p in paths)
                    if not found:
                        print(f"BROKEN: {rel} -> [[{target}#{heading}]] (heading not found)")
                        errors += 1
                else:
                    resolved += 1

            if resolved == 0:
                print(f"MISSING: {rel} — no resolvable wikilinks")
                errors += 1

    if index_count == 0:
        print("No INDEX.md files found.")
        return

    if errors == 0:
        print(f"All {index_count} INDEX.md files pass validation.")
    else:
        print(f"\nFound {errors} issue(s) across {index_count} INDEX.md file(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()