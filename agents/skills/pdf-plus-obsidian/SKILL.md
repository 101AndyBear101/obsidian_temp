---
name: pdf-plus-obsidian
description: Annotate and navigate PDFs with the Obsidian PDF++ community plugin; use for plugin-specific PDF links and sidenotes, not plain embeds or general PDF editing.
status: active
tags:
  - skills/pdf-plus-obsidian
---

# Obsidian PDF++

## Activation Boundary

Use this skill for PDF++-specific PDF selection links, backlink highlights, Markdown sidenotes, or other PDF++ behavior. Do not use it for plain PDF embeds or general PDF editing without the plugin.

Before relying on PDF++ behavior, confirm that the plugin is installed and enabled. Do not install, enable, or configure it unless the user explicitly asks.

## Portable Annotations

Prefer Obsidian-native Markdown links and backlinks to PDF selections, with Markdown sidenotes. Preserve portable annotations in source notes rather than depending on plugin-specific syntax. Use optional PDF++ link parameters only when they are configured and the user requests them.

Validate selection links and rendered highlights in Obsidian. Do not expose sensitive PDF content while quoting, linking, or reporting on annotations.

## File-Modifying Features

Direct PDF annotation, page composition, outline changes, page-label changes, and similar file-modifying features are experimental or high impact. Before using them, require explicit authorization, confirm a backup or recovery path, and verify the PDF and related links after the edit.

PDF++ relies on Obsidian private APIs, so its behavior can change with Obsidian or plugin versions. Treat advanced behavior as version-sensitive.

## Validation

1. Confirm PDF links, highlights, and sidenotes render as expected in Obsidian.
2. Preserve source-note content and verify it remains portable Markdown.
3. After an authorized file modification, reopen the PDF and verify the intended change, its recovery path, and any affected links.

## Upstream Documentation

Use the [PDF++ repository](https://github.com/ryotaushio/obsidian-pdf-plus) and [PDF++ documentation](https://ryotaushio.github.io/obsidian-pdf-plus/) for advanced or version-sensitive behavior.
