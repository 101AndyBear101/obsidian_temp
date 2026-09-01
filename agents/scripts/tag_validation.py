#!/usr/bin/env python3
# agents/scripts/tag_validation.py
"""
Validate tags across all .md files.

Checks:
  - Tags use lowercase-kebab-case
  - Tags use expected prefixes when applicable
  - Reports potential typos or inconsistent tag patterns

Usage: python agents/scripts/tag_validation.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}

KNOWN_PREFIXES = {
    "diagram", "skills", "homelab", "wiki", "journal", "vault", "agent",
    "topic",
}

TAG_RE = re.compile(r"^\s*-\s*(\S+)")


def main():
    errors = 0
    seen_tags = {}

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

            lines = content.splitlines()
            end = 1
            while end < len(lines) and lines[end].strip() != "---":
                end += 1

            in_tags = False
            for line in lines[1:end]:
                if line.strip() == "tags:" or line.strip().startswith("tags:"):
                    in_tags = True
                    # Check inline tags
                    m = re.match(r"tags:\s*\[?(.*?)\]?$", line.strip())
                    if m and m.group(1).strip():
                        for raw_tag in re.findall(r"'([^']+)'|\"([^\"]+)\"|(\S+)", m.group(1)):
                            tag = next(t for t in raw_tag if t)
                            if tag:
                                seen_tags[tag] = seen_tags.get(tag, []) + [rel]
                    continue
                if in_tags and line.strip().startswith("- "):
                    m = TAG_RE.match(line)
                    if m:
                        tag = m.group(1)
                        seen_tags[tag] = seen_tags.get(tag, []) + [rel]
                elif in_tags and not line.strip().startswith("- ") and not line.strip().startswith("#"):
                    in_tags = False

    # Validate each tag
    for tag, files in sorted(seen_tags.items()):
        # Check lowercase-kebab-case
        if not re.match(r"^[a-z0-9][a-z0-9/.-]*$", tag):
            print(f"INVALID: tag '{tag}' — not lowercase kebab-case (used in {len(files)} file(s))")
            errors += 1
            continue

        # Check known prefixes
        if "/" in tag:
            prefix = tag.split("/")[0]
            if prefix not in KNOWN_PREFIXES:
                print(f"UNKNOWN PREFIX: tag '{tag}' — prefix '{prefix}' not in known prefixes {sorted(KNOWN_PREFIXES)} (used in {len(files)} file(s))")
                errors += 1

    # Report tag frequency for review
    print(f"\nTag summary: {len(seen_tags)} unique tags across {sum(len(v) for v in seen_tags.values())} usages")
    for tag, files in sorted(seen_tags.items(), key=lambda x: -len(x[1])):
        print(f"  {tag}: {len(files)} time(s)")

    if errors == 0:
        print("\nAll tags valid.")
    else:
        print(f"\nFound {errors} tag issue(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()