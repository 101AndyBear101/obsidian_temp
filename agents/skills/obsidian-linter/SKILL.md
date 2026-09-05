---
name: obsidian-linter
description: Configure and run Obsidian Linter rules; use for rule-based Markdown, YAML, heading, spacing, and formatting normalization.
status: active
tags:
  - skills/obsidian-linter
---

# Obsidian Linter

## Outcome

Apply deliberate, reviewable formatting rules that keep vault notes consistent without changing their meaning or metadata relationships.

## Activation Boundary

Use this skill for the Obsidian Linter community plugin’s configurable formatting rules and lint commands. Do not use it for semantic content editing, generic prose rewriting, or applying a formatter when Linter is not installed and enabled.

## Workflow

1. Confirm Linter is installed and enabled. Do not install, enable, or reconfigure it unless the user explicitly asks.
2. Inspect active rules, ignored folders, file-level exclusions, custom regex replacements, and custom commands before linting or changing settings.
3. Identify the smallest lint scope: a single note first, then an approved folder or vault-wide operation only when needed.
4. Review interacting rules carefully: overlapping spacing, YAML, heading, or content rules can produce unexpected results.
5. Treat custom regex replacements and custom commands as potentially destructive code. Require explicit authorization and test them on a disposable or version-controlled note before broader use.
6. Back up or confirm version history before an approved multi-file lint operation, then inspect the resulting diff or changed Markdown.

## Validation

1. Confirm the linted note remains valid Markdown with intact frontmatter, links, embeds, and task syntax.
2. Verify changed rules produced the requested formatting without altering note meaning.
3. For folder or vault scopes, inspect representative results and confirm ignored content was not modified.
4. Check the developer console for Linter errors when a lint operation reports a failure.

## Official Sources

- <https://platers.github.io/obsidian-linter/>
- <https://github.com/platers/obsidian-linter>
