#!/usr/bin/env python3
"""Validate reusable base templates and diagram-template fences.

Checks unrendered ``templates/base`` source independently from ordinary notes:
  - balanced YAML frontmatter beginning at the first line
  - required base-template fields and approved Templater date expressions
  - Agent Skill exception fields and its unique skill tag
  - balanced, approved Mermaid or PlantUML fences in diagram templates

Usage: python agents/scripts/template_validation.py
Exit codes: 0 when all checks pass; 1 when any issue is found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
BASE_TEMPLATES = VAULT_ROOT / "templates" / "base"
DIAGRAM_DIRECTORIES = {
    VAULT_ROOT / "templates" / "mermaid_diagrams": "mermaid",
    VAULT_ROOT / "templates" / "plantuml_diagrams": "plantuml",
}
BASE_DATE = '<% tp.file.creation_date("YYYY-MM-DD") %>'
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})([^\s`~]*)[ \t]*$")


def frontmatter_lines(text: str, path: str) -> tuple[list[str], list[str]]:
    """Return frontmatter lines and validation errors without rendering Templater."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], [f"MISSING: {path} — frontmatter must begin with '---'"]
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[1:index], []
    return [], [f"MISSING: {path} — frontmatter has no closing '---'"]


def scalar_fields(lines: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in lines:
        match = re.match(r"^([a-z][a-z0-9-]*):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def tag_values(lines: list[str]) -> list[str]:
    tags: list[str] = []
    collecting = False
    for line in lines:
        if line == "tags:":
            collecting = True
            continue
        if collecting:
            match = re.match(r"^\s+-\s+(.+?)\s*$", line)
            if match:
                tags.append(match.group(1).strip("'\""))
                continue
            break
    return tags


def validate_base_template(path: Path) -> list[str]:
    rel = path.relative_to(VAULT_ROOT).as_posix()
    lines, errors = frontmatter_lines(path.read_text(encoding="utf-8"), rel)
    if errors:
        return errors
    fields = scalar_fields(lines)
    if path.name == "skill-template.md":
        for field in ("name", "description", "status"):
            if not fields.get(field):
                errors.append(f"MISSING: {rel} — skill template requires '{field}'")
        if "kind" in fields or "created" in fields:
            errors.append(f"INVALID: {rel} — Agent Skill templates must not use 'kind' or 'created'")
        if tag_values(lines) != ["skills/skill-name"]:
            errors.append(f"INVALID: {rel} — skill template requires exactly 'skills/skill-name' tag")
        return errors

    for field in ("kind", "status", "created"):
        if not fields.get(field):
            errors.append(f"MISSING: {rel} — template requires '{field}'")
    expected_date = "<% tp.file.title %>" if path.name == "daily-template.md" else BASE_DATE
    if fields.get("created") != expected_date:
        errors.append(f"INVALID: {rel} — 'created' must be '{expected_date}'")
    if path.name == "daily-template.md" and "# <% tp.file.title %>" not in path.read_text(encoding="utf-8"):
        errors.append(f"INVALID: {rel} — daily title must derive from tp.file.title")
    return errors


def diagram_fence_errors(text: str, language: str, rel: str) -> list[str]:
    """Validate diagram fences while distinguishing openers from closing fences."""
    errors: list[str] = []
    openers: list[str] = []
    active_fence: tuple[str, int] | None = None

    for line_number, line in enumerate(text.splitlines(), start=1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        marker, info = match.groups()
        marker_kind = marker[0]

        if active_fence:
            active_kind, active_length = active_fence
            if not info and marker_kind == active_kind and len(marker) >= active_length:
                active_fence = None
            continue

        if not info:
            errors.append(f"INVALID: {rel}:{line_number} — unmatched closing Markdown fence")
            continue
        openers.append(info)
        active_fence = (marker_kind, len(marker))

    if active_fence:
        errors.append(f"INVALID: {rel} — fenced code blocks are unbalanced")
    if language not in openers:
        errors.append(f"INVALID: {rel} — requires a '{language}' fenced diagram block")
    invalid = [opener for opener in openers if opener not in {"mermaid", "plantuml"}]
    if invalid:
        errors.append(f"INVALID: {rel} — unsupported diagram fence language(s): {', '.join(invalid)}")
    return errors


def validate_diagram_template(path: Path, language: str) -> list[str]:
    rel = path.relative_to(VAULT_ROOT).as_posix()
    return diagram_fence_errors(path.read_text(encoding="utf-8"), language, rel)


def regression_check() -> list[str]:
    """Prove malformed source fails without adding a persistent malformed fixture."""
    _, errors = frontmatter_lines("kind: note\n---\n", "in-memory-fixture.md")
    if errors:
        errors = []
    else:
        errors = ["INTERNAL: malformed-frontmatter regression case did not fail"]
    fence_errors = diagram_fence_errors("```\n", "mermaid", "in-memory-fence.md")
    if not any("unmatched closing Markdown fence" in error for error in fence_errors):
        errors.append("INTERNAL: unmatched-closing-fence regression case did not fail")
    return errors


def main() -> int:
    errors = regression_check()
    for path in sorted(BASE_TEMPLATES.glob("*.md")):
        errors.extend(validate_base_template(path))
    for directory, language in DIAGRAM_DIRECTORIES.items():
        for path in sorted(directory.glob("*.md")):
            if path.name in {"INDEX.md", "README.md"}:
                continue
            errors.extend(validate_diagram_template(path, language))

    if errors:
        print("\n".join(errors))
        print(f"\nFound {len(errors)} template validation issue(s).")
        return 1
    print("All base templates and diagram fences passed validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
