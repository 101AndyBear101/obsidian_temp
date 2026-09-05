---
name: obsidian-quickadd
description: Create and maintain Obsidian QuickAdd choices; use for template, capture, macro, and multi workflows that automate note creation or capture.
status: active
tags:
  - skills/obsidian-quickadd
---

# Obsidian QuickAdd

## Outcome

Create a focused QuickAdd workflow that captures or creates the intended vault content while preserving existing notes and templates.

## Activation Boundary

Use this skill for QuickAdd template, capture, macro, or multi choices. Do not use it for ordinary manual note creation, core Templates configuration, or unreviewed JavaScript automation outside a QuickAdd workflow.

## Workflow

1. Confirm QuickAdd is installed and enabled. Do not install, enable, or configure it unless the user explicitly asks.
2. Choose the smallest suitable choice type: template for a new note, capture for appending to a known target, macro for an approved sequence, or multi for organizing choices.
3. Confirm target files, folders, templates, insertion points, and filename syntax before creating or modifying a choice.
4. Preserve valid vault metadata and use the existing PARA folders and templates where applicable.
5. Treat macros and user scripts as code: review every action, require explicit authorization for file-moving, bulk-editing, network, or system-command behavior, and do not execute untrusted code.
6. Test the choice with a disposable note or reversible capture before relying on it for routine use.

## Validation

1. Confirm the choice creates or captures content only at the requested target.
2. Inspect the resulting Markdown, frontmatter, and links for vault-convention compliance.
3. Confirm macros run in the intended sequence and do not modify files outside the approved scope.

## Official Source

- <https://github.com/chhoumann/quickadd>
