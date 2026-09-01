#!/usr/bin/env python3
# agents/scripts/check_wikilinks.py
"""
Check all [[wikilinks]] across the vault and report broken ones.

Handles:
  - Plain links: [[note-name]]
  - Aliased links: [[note-name|Display Text]]
  - Path-qualified: [[dir/note-name]]
  - Section links: [[note-name#Heading]]
  - Embeds: ![[note-name]]
  - Skips external URLs, email links, attachment/Base files (.png, .pdf, .base, etc.)
  - Skips placeholder links in templates, plans, and skill documentation

Usage: python agents/scripts/check_wikilinks.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}

NON_NOTE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp",
                 ".pdf", ".mp3", ".ogg", ".wav", ".base", ".canvas",
                 ".yaml", ".yml", ".json", ".xml", ".csv", ".tsv",
                 ".zip", ".tar", ".gz", ".py", ".sh"}

LINK_RE = re.compile(r"(?<!!)\[\[([^]]+)\]\]")

PLACEHOLDER_PATTERNS = r"(?:parent-resource-name|related-note|note-name|project-name|resource-name|area-name|skill-name|diagram-type-diagram|YYYY-MM-DD)"

PLACEHOLDER_TARGETS = {
    "note", "embed", "wikilinks", "note name", "mybase",
    "my base", "image", "document", "algorithm notes",
    "architecture diagram", "meeting notes", "meeting notes 2024-01-10",
    "other note", "improve workflow", "basefile",
    "...", "[your other note",
}


def _split_target(raw: str) -> tuple:
    """Split [[target|alias]] into (target_name, heading_or_None)."""
    # Handle escaped pipe (\\|) used in markdown tables
    if "\\|" in raw:
        raw = raw.split("\\|")[0]
    elif "|" in raw:
        raw = raw.split("|")[0]
    heading = None
    if "#" in raw:
        raw, heading = raw.rsplit("#", 1)
    return raw, heading or None


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
    errors = set()

    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, VAULT_ROOT).replace("\\", "/")

            with open(fpath, encoding="utf-8") as f:
                content = f.read()

            for match in LINK_RE.finditer(content):
                raw = match.group(1)
                target, heading = _split_target(raw)

                if re.match(r"^(https?|mailto):", target, re.IGNORECASE):
                    continue
                if not target:
                    continue

                # Skip placeholder targets
                if target.lower().strip() in PLACEHOLDER_TARGETS:
                    continue
                if re.search(PLACEHOLDER_PATTERNS, target, re.IGNORECASE):
                    continue

                paths = _resolve_file(target)
                if not paths:
                    key = f"{rel} -> [[{raw}]]"
                    if key not in errors:
                        print(f"BROKEN: {rel} -> [[{raw}]]")
                        errors.add(key)
                    continue

                if heading:
                    found = any(_heading_exists(p, heading) for p in paths)
                    if not found:
                        key = f"{rel} -> [[{target}#{heading}]]"
                        if key not in errors:
                            print(f"BROKEN: {rel} -> [[{target}#{heading}]] (heading not found)")
                            errors.add(key)

    if not errors:
        print("All wikilinks resolve.")
    else:
        print(f"\nFound {len(errors)} broken link(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()