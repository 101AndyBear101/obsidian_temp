---
name: day-planner-obsidian
description: Plan time-blocked daily-note tasks with the Obsidian Day Planner community plugin; use for timeline behavior, not generic tasks or calendar notes.
status: active
tags:
  - skills/day-planner-obsidian
---

# Obsidian Day Planner

## Activation Boundary

Use this skill when the user asks to plan or render a daily timeline with the Obsidian Day Planner community plugin. Do not use it for generic task lists, ordinary calendar notes, or plain Markdown checkboxes without Day Planner behavior.

Before relying on a timeline, confirm that Day Planner is installed and enabled, and that its Daily Notes or Periodic Notes prerequisite is available in the vault. Do not install, enable, configure, or guess plugin settings unless the user explicitly asks.

## Author Time Blocks

Write time-blocked tasks in the relevant daily note using the documented format:

```markdown
- [ ] 09:00 - 10:00 Prepare the weekly review
```

Preserve the source task text and checkbox state. Use the plugin’s UI or commands for interactive timeline edits rather than inferring its configuration from note text.

## Tasks Integration and Calendar Feeds

Tasks-plugin integration requires scheduled tasks and may show matching tasks from elsewhere in the vault. Confirm the integration and its current settings before relying on that behavior; do not alter a source task merely to make it appear on a timeline.

Online ICS feed URLs can include private calendar access tokens. Do not add, expose, or copy an ICS URL without the user’s explicit authorization.

Time tracking is experimental and may be version-sensitive. Confirm the installed plugin version and consult upstream documentation before relying on it for automated or authoritative records.

## Validation

1. Confirm the time blocks render on the intended Day Planner timeline in Live Preview or Reading View.
2. Check the daily note after interactive edits to ensure its source task text and state match the user’s intent.
3. When Tasks integration is in scope, verify which scheduled tasks appear and whether results span other vault notes.

## Upstream Documentation

Use the [Day Planner repository](https://github.com/ivan-lednev/obsidian-day-planner) for advanced or version-sensitive behavior.
