#!/usr/bin/env python3
"""Audit a flat Agent Skills directory against INDEX.md.

Emits JSON to stdout and diagnostics to stderr. The script is read-only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIELD_PATTERN = re.compile(r"(?m)^(name|description|status):\s*(.+?)\s*$")
TAG_BLOCK_PATTERN = re.compile(r"(?m)^tags:\s*\n((?:[ \t]+-\s*.+\n?)*)")
TAG_ITEM_PATTERN = re.compile(r"(?m)^[ \t]+-\s*(.+?)\s*$")


def strip_yaml_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_skill(path: Path) -> tuple[dict[str, str], list[str]]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, re.DOTALL)
    if not match:
        return {}, ["missing_or_malformed_frontmatter"]
    frontmatter = match.group(1)
    fields = {key: strip_yaml_value(value) for key, value in FIELD_PATTERN.findall(frontmatter)}
    tag_match = TAG_BLOCK_PATTERN.search(frontmatter)
    tags = [] if not tag_match else [strip_yaml_value(value) for value in TAG_ITEM_PATTERN.findall(tag_match.group(1))]
    fields["tags"] = "\n".join(tags)
    if "[TODO" in text:
        issues.append("unfinished_placeholder")
    return fields, issues


def indexed_names(index_path: Path) -> set[str]:
    if not index_path.exists():
        return set()
    names: set[str] = set()
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\|\s*`?([a-z0-9][a-z0-9-]*)`?\s*\|", line)
        if match and match.group(1) != "Skill":
            names.add(match.group(1))
    return names


def audit(skills_root: Path) -> dict[str, object]:
    index_path = skills_root / "INDEX.md"
    index_names = indexed_names(index_path)
    findings: list[dict[str, object]] = []
    collections: list[dict[str, object]] = []
    discovered_names: set[str] = set()

    for folder in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        skill_path = folder / "SKILL.md"
        item: dict[str, object] = {"folder": folder.name, "path": str(folder), "issues": []}
        issues: list[str] = item["issues"]  # type: ignore[assignment]
        if not skill_path.exists():
            nested_skills = sorted(str(path.relative_to(folder)) for path in folder.glob("skills/*/SKILL.md"))
            if nested_skills:
                collections.append({"folder": folder.name, "path": str(folder), "nested_skills": nested_skills})
                continue
            issues.append("missing_SKILL.md")
            findings.append(item)
            continue

        discovered_names.add(folder.name)
        fields, parse_issues = parse_skill(skill_path)
        issues.extend(parse_issues)
        name = fields.get("name", "")
        description = fields.get("description", "")
        status = fields.get("status", "")
        tags = fields.get("tags", "").splitlines()
        item["name"] = name
        item["description_length"] = len(description)
        if not name:
            issues.append("missing_name")
        elif name != folder.name:
            issues.append("name_does_not_match_folder")
        elif len(name) > 64 or not NAME_PATTERN.fullmatch(name):
            issues.append("invalid_name")
        if not description:
            issues.append("missing_description")
        elif len(description) > 1024:
            issues.append("description_too_long")
        if not status:
            issues.append("missing_status")
        expected_tag = f"skills/{folder.name}"
        if tags != [expected_tag]:
            issues.append("missing_or_malformed_skill_tag")
        if folder.name not in index_names:
            issues.append("missing_from_skills_index")
        findings.append(item)

    stale_index_entries = sorted(index_names - discovered_names)
    return {
        "skills_root": str(skills_root),
        "index_path": str(index_path),
        "index_exists": index_path.exists(),
        "skills_found": len(findings),
        "findings": findings,
        "imported_collections": collections,
        "stale_index_entries": stale_index_entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Agent Skills folders against INDEX.md.")
    parser.add_argument("--skills-root", required=True, help="Path containing direct child skill folders.")
    args = parser.parse_args()
    root = Path(args.skills_root).resolve()
    if not root.is_dir():
        print(f"Error: --skills-root is not a directory: {root}", file=sys.stderr)
        return 2
    print(json.dumps(audit(root), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
