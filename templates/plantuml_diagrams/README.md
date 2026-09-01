---
kind: guide
status: active
created: 2026-08-25
tags:
  - plantuml
---

# PlantUML Diagram Templates

This folder contains self-contained PlantUML templates for use in Obsidian notes. Open [[templates/plantuml_diagrams/INDEX|the template index]] to choose a diagram by purpose.

## How to Use a Template

1. Copy the template into the relevant note.
2. Replace example labels and relationships with the information the note needs.
3. Keep the diagram inside a `plantuml` fenced block.
4. Render it in Obsidian before relying on it in a wiki note.

Most templates use `@startuml` and `@enduml`. Use the diagram-specific envelope already provided by templates such as Gantt, mind maps, NWDiag, and Ditaa; do not replace it with the generic form.

## Rendering Notes

- A renderer may send diagram source to a remote service; use a local renderer for sensitive homelab diagrams.
- Ditaa uses `@startditaa` and `@endditaa`, and it must render as PNG rather than SVG.
- NWDiag uses `@startnwdiag` and `@endnwdiag`.
- The ArchiMate template uses a PlantUML standard-library include, so it requires renderer access to that library.

## Authoring Guidance

Use concise labels, stable aliases, and a single clear purpose per diagram. Do not include passwords, tokens, private keys, or other sensitive configuration values. For detailed authoring and troubleshooting guidance, use the vault's `plantuml-diagrams` and `plantuml-obsidian` skills.
