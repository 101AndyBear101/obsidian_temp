#!/usr/bin/env python3
# agents/scripts/attachment_validation.py
"""
Find unreferenced files in files/ and broken embed targets in notes.

Checks:
  - Files in files/ that no note links to or embeds
  - Embed targets (![[file.png]], ![[document.pdf]]) that don't exist

Skips:
  - Placeholder embeds in skill documentation and reference files
  - Path-qualified embeds are resolved correctly

Usage: python agents/scripts/attachment_validation.py
"""

import os
import re
import sys

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}
FILES_DIR = os.path.join(VAULT_ROOT, "files")

EMBED_RE = re.compile(r"!\[\[([^]]+)\]\]")
LINK_RE = re.compile(r"(?<!!)\[\[([^]]+)\]\]")

PLACEHOLDER_PATTERNS = r"(?:proxmox-nfs-settings|note|embed|MyBase|Note Name|image\.png|document\.pdf|audio\.mp3|audio\.ogg|Architecture Diagram|BaseFile|baseFile)"
PLACEHOLDER_TARGETS = {"embed", "note", "wikilinks", "note name", "file"}


def _resolve_embed_path(target: str) -> str:
    """Resolve an embed target to an absolute path."""
    # Skip pipes and heading fragments
    target = target.split("|")[0].split("#")[0]

    if "/" in target:
        full = os.path.join(VAULT_ROOT, target)
        # Could be with or without extension
        if os.path.exists(full):
            return full
    else:
        # Search for matching file anywhere
        for root, dirs, files in os.walk(VAULT_ROOT):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if f == target or f == target.split("/")[-1]:
                    return os.path.join(root, f)
        # Try as .md file
        md_target = target if target.endswith(".md") else target + ".md"
        for root, dirs, files in os.walk(VAULT_ROOT):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if f == md_target:
                    return os.path.join(root, f)
    return None


def main():
    errors = 0

    # Build set of all files in files/
    attachments = set()
    if os.path.exists(FILES_DIR):
        for root, dirs, files in os.walk(FILES_DIR):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), VAULT_ROOT).replace("\\", "/")
                attachments.add(rel)

    # Build set of all referenced attachments
    referenced = set()
    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, VAULT_ROOT).replace("\\", "/")

            # Skip skill documentation and reference files — they use placeholder embeds
            if "/references/" in rel or "/skills/" in rel:
                continue

            with open(fpath, encoding="utf-8") as f:
                content = f.read()

            for match in EMBED_RE.finditer(content):
                target = match.group(1)

                # Skip placeholder targets
                if target.lower().strip() in PLACEHOLDER_TARGETS:
                    continue
                if re.search(PLACEHOLDER_PATTERNS, target, re.IGNORECASE):
                    continue

                resolved = _resolve_embed_path(target)
                if not resolved:
                    print(f"BROKEN EMBED: {rel} -> ![[{target}]] (file not found)")
                    errors += 1
                else:
                    referenced.add(target)

            for match in LINK_RE.finditer(content):
                target = match.group(1).split("|")[0].split("#")[0]
                if re.search(PLACEHOLDER_PATTERNS, target, re.IGNORECASE):
                    continue
                if target.lower().strip() in PLACEHOLDER_TARGETS:
                    continue
                referenced.add(target)

    # Find attachments not referenced
    referenced_basenames = {r.split("/")[-1] for r in referenced}
    referenced_stems = {os.path.splitext(r)[0] for r in referenced_basenames}
    for att in sorted(attachments):
        basename = os.path.basename(att)
        stem = os.path.splitext(basename)[0]
        if stem not in referenced_stems and basename not in referenced_basenames:
            print(f"UNREFERENCED: {att} — no note links to or embeds this file")
            errors += 1

    if errors == 0:
        print("All attachments referenced and all embeds resolve.")
    else:
        print(f"\nFound {errors} attachment/embed issue(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()