#!/usr/bin/env python3
"""Remove completed ``internal_prompt`` fences from one Markdown file.

Agents should write their answer below each prompt fence before running this
script. Only complete ``internal_prompt`` blocks are removed; all surrounding
Markdown, including the answer beneath the block, remains unchanged.

Usage:
    python agents/scripts/remove_internal_prompts/remove_internal_prompts.py path/to/note.md
    python agents/scripts/remove_internal_prompts/remove_internal_prompts.py --dry-run path/to/note.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

OPEN_FENCE_RE = re.compile(
    r"^ {0,3}(?P<fence>`{3,}|~{3,})internal_prompt[ \t]*$"
)


def remove_internal_prompts(text: str) -> tuple[str, int]:
    """Return text without complete internal_prompt fences and their count.

    Raises:
        ValueError: If an internal_prompt fence has no matching closing fence.
    """
    lines = text.splitlines(keepends=True)
    result: list[str] = []
    index = 0
    removed = 0

    while index < len(lines):
        opener = OPEN_FENCE_RE.fullmatch(lines[index].rstrip("\r\n"))
        if not opener:
            result.append(lines[index])
            index += 1
            continue

        fence = opener.group("fence")
        closing_fence_re = re.compile(
            rf"^ {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*$"
        )
        closing_index = next(
            (
                candidate
                for candidate in range(index + 1, len(lines))
                if closing_fence_re.fullmatch(lines[candidate].rstrip("\r\n"))
            ),
            None,
        )
        if closing_index is None:
            raise ValueError(
                f"Unclosed internal_prompt fence beginning on line {index + 1}."
            )

        removed += 1
        index = closing_index + 1
        if result and not result[-1].strip() and index < len(lines) and not lines[index].strip():
            index += 1

    return "".join(result), removed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove complete internal_prompt blocks from a Markdown file."
    )
    parser.add_argument("path", type=Path, help="Markdown file to update")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report how many blocks would be removed without changing the file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.path.is_file():
        print(f"ERROR: Markdown file not found: {args.path}", file=sys.stderr)
        return 2

    try:
        original = args.path.read_text(encoding="utf-8")
        updated, removed = remove_internal_prompts(original)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"Would remove {removed} internal_prompt block(s) from {args.path}.")
        return 0

    if removed:
        args.path.write_text(updated, encoding="utf-8")
    print(f"Removed {removed} internal_prompt block(s) from {args.path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
