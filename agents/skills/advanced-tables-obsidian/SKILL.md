---
name: advanced-tables-obsidian
description: Author and safely edit Markdown tables with the Obsidian Advanced Tables community plugin; use for plugin-assisted tables, not spreadsheets or ordinary tables.
status: active
tags:
  - skills/advanced-tables-obsidian
---

# Obsidian Advanced Tables

## Activation Boundary

Use this skill for Markdown tables that need the Obsidian Advanced Tables community plugin’s interactive behavior. Do not use it for spreadsheet files or ordinary static Markdown tables when no plugin command is needed.

Before relying on interactive commands, confirm that Advanced Tables is installed and enabled. Do not install, enable, or configure the plugin unless the user explicitly asks.

## Author Stable Tables

Write standards-compliant Markdown tables with a header row, separator row, and stable columns:

```markdown
| Task | Owner | Status |
| --- | --- | --- |
| Review notes | Alex | Active |
```

Preserve the table’s existing meaning, column order, and data. Do not introduce formula syntax unless the user specifically requests formulas.

## Interactive Operations

Use formatting, navigation, row or column operations, sorting, formulas, or CSV export only when requested. Treat batch or structural table changes cautiously: the plugin documents possible note-data instability. Confirm backups or version history are available before making destructive-looking transformations.

After interactive edits, reread the changed Markdown rather than assuming the rendered result is the saved source.

## Validation

1. Confirm the table renders correctly in Obsidian.
2. Reread the changed Markdown and verify headers, columns, and values remain aligned with the original intent.
3. For batch or structural changes, confirm the requested scope and available recovery path before editing.

## Upstream Documentation

Use the [Advanced Tables repository](https://github.com/tgrosinger/advanced-tables-obsidian) and its upstream documentation for version-sensitive commands.
