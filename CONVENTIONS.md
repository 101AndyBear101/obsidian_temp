# Conventions

## Overview

This document is the single source of truth for the Obsidian Template Vault's schema, naming conventions, and routing rules.

## Folder Roles

| Role | Description | Example |
|------|-------------|---------|
| `bases/` | Structured views and queryable dashboards | `bases/overview.md` |
| `journals/` | Time-based capture (daily notes) | `journals/daily/2026-08-25.md` |
| `areas/` | Ongoing responsibilities without an end date | `areas/homelab.md` |
| `projects/` | Finite-effort initiatives with a defined outcome | `projects/homelab-docs.md` |
| `resources/` | Reusable collections of related notes | `resources/homelab-ops.md` |
| `notes/` | Atomic source notes and contextual wiki notes | `notes/homelab-overview.md` |
| `canvases/` | Spatial maps and visual working surfaces | `canvases/home-lab-map.md` |
| `files/` | Attachments and supporting non-note assets | `files/homelab-config.yaml` |
| `plans/` | Reviewable plans for structural changes | `plans/guidance-adjustment-plan.md` |
| `templates/` | Reusable note and diagram templates | `templates/base/notes-template.md` |

## Areas

> An **area** is an ongoing domain of responsibility with no defined end date. It defines the standards, routines, boundaries, and long-term outcomes for that domain.

Examples include caring for your home, managing work, handling money, and looking after your health.

An area can provide durable context for multiple finite **projects**. Use an area when the responsibility continues after individual projects finish; use a project when the work has a defined, completable outcome.

## Projects

> A **project** is a finite initiative with a specific, measurable outcome. It ends when that outcome is completed, abandoned, or paused.

Examples include fixing a leaky faucet, planning a vacation, preparing taxes, and applying for a new job.

A project may identify one parent **area** when that context is useful. Projects can use **resources** for reusable reference material and focused **notes** for canonical knowledge, decisions, and procedures.

## Resources

> A **resource** is a reusable collection of related notes about a subject, practice, or body of knowledge. It provides context and organization without duplicating canonical note content.

Examples include a recipe collection, a home-repair guide, or a travel-planning reference.

A resource can support multiple **projects**, and a focused **note** can belong to multiple resources. For example, a note about making bread can belong to both a recipes resource and a home-skills resource. Express each note's memberships through its `resource` frontmatter list; link the canonical note to every relevant resource rather than copying it.

## Notes

> A **note** is one focused, reusable piece of knowledge. It answers one question, records one decision, explains one procedure, or captures one concept. Notes are the canonical source of the actual information; resources organize and contextualize them.

Notes should be atomic: each note covers one subject, question, decision, procedure, or concept that can be understood and reused independently. Examples include how to fix a leaky faucet, a vacation packing checklist, how to make bread, or the steps for preparing taxes. A note can belong to multiple resources when the same knowledge is useful in more than one context.

## Relationship Hierarchy

```text
area
└── projects (optional, many per area)
    └── resources (optional, many per project)
        └── notes (optional, many per resource)
```

All relationship properties are recommended rather than required. A missing relationship produces a validation recommendation. Values are compact lowercase identifiers containing letters, numbers, hyphens, or underscores, with no spaces. They do not need to match filenames or resolve to files. Identifiers longer than 20 characters produce a warning.

## Metadata Schema

Ordinary vault notes must include these core metadata fields. Agent Skills use the documented exception in [[CONVENTIONS#Agent Skill Frontmatter]].

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `kind` | lowercase kebab-case string | Yes | Note type: `note`, `project`, `resource`, `area`, `plan`, `index`, `guide`, `template` |
| `status` | lowercase kebab-case string | Yes | Lifecycle state: `active`, `paused`, `complete`, `archive` |
| `created` | Real ISO date (`YYYY-MM-DD`) | Yes | Creation date of the note; future dates are allowed |
| `tags` | list of compact lowercase tags | Recommended | Single-level or slash-separated topics; missing tags produce a recommendation |
| `area` | compact lowercase string | Recommended | Related area for a project |
| `project` | list of compact lowercase strings | Recommended | Related projects for a resource |
| `resource` | list of compact lowercase strings | Recommended | Related resources for a note |

## Kind-Specific Requirements

| Kind | Required Properties | Optional Properties |
| --- | --- | --- |
| `note` | `kind`, `status`, `created` | Recommended: `type` (permanent/fleeting/contextual/diagram/journal), `resource`, `tags` |
| `project` | `kind`, `status`, `created` | Recommended: `area`, `tags` |
| `resource` | `kind`, `status`, `created` | Recommended: `project`, `tags` |
| `area` | `kind`, `status`, `created` | Recommended: `tags` |
| `plan` | `kind`, `status`, `created` | Recommended: `tags` |
| Agent Skill | See [[CONVENTIONS#Agent Skill Frontmatter]] | N/A |
| `guide` | `kind`, `status`, `created` | Recommended: `tags` |
| `index` | `kind`, `status`, `created` | Recommended: `tags` |
| `template` | `kind`, `status`, `created` | Recommended: `tags` |

## Relationship Properties

- **`area`**: Recommended scalar compact identifier (e.g., `home_ops`); identifies a project's related area.
- **`project`**: Recommended list of compact identifiers (e.g., `["vault_tools"]`); identifies a resource's related projects.
- **`resource`**: Recommended list of compact identifiers (e.g., `["python-validation"]`); identifies a note's related resources. A direct `project` or `area` value on a note remains optional supplementary metadata when useful for filtering or discovery.

Compact relationship identifiers match `^[a-z0-9]+(?:[-_][a-z0-9]+)*$`. Tags use one or more compact identifiers separated by `/`, with no fixed hierarchy depth. A complete tag longer than 30 characters produces a warning.

## Agent Skill Frontmatter

`agents/skills/<skill-name>/SKILL.md` is a documented exception to the ordinary vault-note schema. It must contain `name`, `description`, and `status`, plus exactly one `tags` value of `skills/<skill-name>`. The `name` and tag suffix must exactly match the skill folder name. Agent Skills do not require `kind` or `created`; this avoids retrofitting invented metadata into imported third-party skills.

## Naming Patterns

| Pattern | Kind | Example |
|---------|------|--------|
| `area-name` | `kind: area` | `homelab.md` |
| `project-name` | `kind: project` | `homelab-documentation-baseline.md` |
| `resource-name` | `kind: resource` | `homelab-operations-reference.md` |
| `subject-name` | `kind: note` | `fix-leaky-faucet.md` |
| `diagram-type-diagram` | `kind: note, type: diagram` | `service-interaction-sequence-diagram.md` |

## Naming Rules

- Use lowercase kebab-case for all filenames and folder names
- Prefer specific subjects over generic names (`network-storage-overview.md` vs `notes.md`)
- Use singular nouns for single items, plural for collections
- Avoid dates, versions, and status words in ordinary filenames; use `status` in frontmatter instead
- Daily notes are the exception: store them in `journals/daily/` with a real `YYYY-MM-DD.md` filename
- Reserve `AGENTS.md`, `INDEX.md`, `README.md`, and `SKILL.md` for their established purposes

## Routing Content

Place content in the folder whose primary role matches the note's purpose:

| Content Type | Primary Folder | Reason |
|--------------|----------------|---------|
| Daily entries | `journals/daily/` | Time-bound, chronological capture |
| Ongoing responsibilities | `areas/` | Continuous work without deadline |
| Finite projects | `projects/` | Defined start/end with measurable outcome |
| Reference material | `resources/` | Persistent, reusable knowledge |
| Atomic ideas | `notes/` | Self-contained, reusable concepts |
| Visual maps | `canvases/` | Spatial arrangements requiring layout |
| Supporting assets | `files/` | Non-notes (images, docs, scripts) |
| Structural plans | `plans/` | Future-oriented, reviewable work |
| Reusable templates | `templates/` | Shared structures for new content |

## Status Flow

- `active` → `paused` or `complete` → `archive`
- A note may return from `paused` to `active` when work resumes.
- `complete` remains visible in dashboards; `paused` indicates deferred work.
- `archive` excludes content from active dashboards and Base views.
