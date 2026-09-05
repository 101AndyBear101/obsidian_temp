---
name: obsidian-tasknotes
description: Create and manage TaskNotes task notes and Bases views; use for per-task Markdown files, task metadata, recurrence, scheduling, and TaskNotes views.
status: active
tags:
  - skills/obsidian-tasknotes
---

# Obsidian TaskNotes

## Outcome

Manage TaskNotes tasks as portable Markdown notes with valid, consistent frontmatter and appropriately scoped Bases views.

## Activation Boundary

Use this skill for the TaskNotes community plugin’s task-note structure, task views, recurrence, scheduling, time tracking, or TaskNotes-specific task metadata. Do not use it for generic checkbox tasks, the separate Obsidian Tasks plugin, or generic Bases work without a TaskNotes task model.

## Workflow

1. Confirm TaskNotes and its Bases dependency are installed and enabled. Do not install, enable, or reconfigure either plugin unless the user explicitly asks.
2. Inspect the existing TaskNotes folder, configured property names, task template, statuses, and views before creating or modifying tasks.
3. Use the plugin’s task-creation workflow or preserve the existing task-note schema when editing Markdown directly; do not invent field names when the vault has configured mappings.
4. Keep task notes portable: represent task data in YAML frontmatter and preserve human-readable Markdown content.
5. Before changing recurrence, dependencies, time entries, calendars, webhooks, or external synchronization, confirm the requested scope and recovery path. Never add OAuth credentials, webhook secrets, or private calendar-feed URLs to a note.
6. For bulk task changes, confirm the affected task set and obtain explicit approval before applying the mutation.

## Validation

1. Confirm task frontmatter matches the vault’s configured TaskNotes schema.
2. Verify the intended task appears correctly in the relevant TaskNotes or Bases view.
3. For recurring or scheduled work, confirm dates, instances, and status behavior match the user’s intent.
4. After a bulk or integration-related change, verify the source task notes and affected views.

## Official Source

- <https://github.com/callumalpass/tasknotes>
