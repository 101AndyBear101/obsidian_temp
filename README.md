---
kind: guide
status: active
created: 2026-08-25
tags:
  - vault/onboarding
---

# Obsidian Template Vault

A reusable, privacy-safe starting point for a personal knowledge system organized around PARA: projects, areas, resources, and archives. The role-based root folders are stable and are used by the included templates and Base views.

## Start Here

1. Create an area for an ongoing responsibility in `areas/`.
2. Create a project with a finite outcome in `projects/`, and associate it with an area.
3. Collect reference material in `resources/`.
4. Keep canonical knowledge in focused source notes in `notes/`; use contextual overview notes to connect and embed that knowledge for a specific task.
5. Use the templates in `templates/` when creating notes.

The fictional [[areas/homelab|homelab area]] demonstrates the complete hierarchy. It contains the [[projects/homelab-documentation-baseline|homelab documentation baseline]] and [[projects/homelab-wiki-launch|homelab wiki launch]] projects, which connect to [[resources/homelab-operations-reference|homelab operations]] and [[resources/wiki-authoring-reference|wiki authoring]] resources. Start with [[notes/homelab-overview|the homelab overview]] or [[notes/wiki-overview|the wiki overview]] to see contextual notes embedding canonical atomic-note sections.

See [[CONVENTIONS]] for folder roles, metadata schema, naming patterns, and routing rules.

## Templates and Plugins

The core **Templates** plugin should use `templates/` as its template folder. The included **Templater** community plugin is configured for the same folder and powers the dynamic fields in the base templates. Use **Calendar** with Daily Notes if you want calendar-based access to journal entries.

Other installed community plugins, such as PDF++, are optional. Keep a plugin only when it supports your own workflow; templates that depend on a plugin say so in their folder guidance.

Use [[templates/base/notes-template|the notes template]] for atomic source notes. For a contextual wiki note, set `type: contextual`, explain its audience or task, and embed only stable headings from the canonical source notes. The [[notes/homelab-overview|homelab overview]] and [[notes/wiki-overview|wiki overview]] demonstrate this pattern.

> [!tip]
> The example notes are fictional and safe to replace or remove after you understand the structure.
