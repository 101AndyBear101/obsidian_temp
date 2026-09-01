---
kind: note
resource:
  - wiki-authoring-reference
status: active
type: permanent
created: 2026-08-25
tags:
  - wiki/content
---

# Wiki Content Standard

## Purpose

Define a predictable structure for contextual wiki pages built from canonical source notes.

## Page Standard

Each contextual wiki page should:

1. State its audience or operational purpose near the top.
2. Link to the relevant area, project, and resource where useful.
3. Embed stable `##` headings from atomic source notes instead of copying canonical instructions.
4. Add local explanation only when it helps the page's specific audience or task.
5. End with related links that support navigation without duplicating metadata.

Use a descriptive `<subject>-overview.md` filename and set `type: contextual`.

## Validation

A page meets the standard when canonical instructions have one source, all embeds resolve, and a reader can navigate back to the resource or project that gives the page context.

## Related

- [[resources/wiki-authoring-reference|Wiki authoring reference]]
- [[projects/homelab-wiki-launch|Homelab wiki launch]]
- [[notes/wiki-overview|Wiki overview]]
