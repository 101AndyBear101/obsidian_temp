---
kind: guide
status: active
created: 2026-08-25
tags:
  - mermaid
---
# Mermaid Diagram Templates

This folder contains self-contained Mermaid templates for use in Obsidian notes. Open [[templates/mermaid_diagrams/INDEX|the template index]] to choose a diagram by purpose.

## How to Use a Template

1. Copy the template into the relevant note.
2. Replace the example labels and relationships with the information the note needs.
3. Keep the diagram inside a `mermaid` fenced block.
4. Render it in Obsidian before relying on it in a wiki note.

## Rendering Notes

- Start with flowchart, sequence, state, ER, or Gantt diagrams for the most reliable cross-renderer support.
- Treat internal hostnames, addresses, and architecture details as sensitive when a remote renderer is in use.
- Advanced Mermaid diagram types can vary by renderer version; verify them in Obsidian before using them as canonical wiki documentation.

## Authoring Guidance

Use simple identifiers and specific labels. Keep each diagram focused on one relationship, process, plan, or data model. Do not include passwords, tokens, private keys, or other sensitive configuration values. For detailed authoring and troubleshooting guidance, use the vault's `mermaid-diagrams` skill.
