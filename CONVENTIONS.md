# Conventions

## Overview

This document is the single source of truth for the Obsidian Template Vault's schema, naming conventions, and routing rules.

## Folder Roles

| Role | Description | Example |
|------|-------------|---------|
| `bases/` | Structured views and queryable dashboards | `bases/overview.md` |
| `journals/` | Time-based capture (daily notes) | `journals/days/2026-08-25.md` |
| `areas/` | Ongoing responsibilities without an end date | `areas/homelab.md` |
| `projects/` | Finite-effort initiatives with a defined outcome | `projects/homelab-docs.md` |
| `resources/` | Reference material and reusable learning | `resources/homelab-ops.md` |
| `notes/` | Atomic source notes and contextual wiki notes | `notes/homelab-overview.md` |
| `canvases/` | Spatial maps and visual working surfaces | `canvases/home-lab-map.md` |
| `files/` | Attachments and supporting non-note assets | `files/homelab-config.yaml` |
| `plans/` | Reviewable plans for structural changes | `plans/guidance-adjustment-plan.md` |
| `templates/` | Reusable note and diagram templates | `templates/base/notes-template.md` |

## Metadata Schema

Ordinary vault notes must include these core metadata fields. Agent Skills use the documented exception in [[CONVENTIONS#Agent Skill Frontmatter]].

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `kind` | lowercase kebab-case string | Yes | Note type: `note`, `project`, `resource`, `area`, `index`, `guide`, `template`, `archive` |
| `status` | lowercase kebab-case string | Yes | Lifecycle state: `active`, `paused`, `complete`, `archive` |
| `created` | ISO date (`YYYY-MM-DD`) | Yes | Creation date of the note |
| `tags` | list of lowercase keywords | Optional | Topics or categories for grouping |
| `area` | plain lowercase-kebab-case filename | Conditional | Parent area for a project |
| `project` | list of plain lowercase-kebab-case filenames | Conditional | Parent projects for a resource |
| `resource` | list of plain lowercase-kebab-case filenames | Conditional | Parent resources for a note |

## Kind-Specific Requirements

| Kind | Required Properties | Optional Properties |
|------|---------------------|----------------------|
| `note` | `kind`, `status`, `created`, `resource` | `type` (permanent/fleeting/contextual/diagram), `tags` |
| `project` | `kind`, `status`, `created`, `area` | `tags` |
| `resource` | `kind`, `status`, `created`, `project` | `tags` |
| `area` | `kind`, `status`, `created` | `tags` |
| Agent Skill | See [[CONVENTIONS#Agent Skill Frontmatter]] | N/A |
| `guide` | `kind`, `status`, `created` | `tags` |
| `index` | `kind`, `status`, `created` | `tags` |
| `template` | `kind`, `status`, `created` | `tags` |

## Relationship Properties

- **`area`**: Scalar plain lowercase-kebab-case filename without `.md` (e.g., `homelab`); the parent-area relationship for a project.
- **`project`**: List of bare lowercase-kebab-case filenames without `.md` (e.g., `["homelab-documentation-baseline"]`); the parent-project relationship for a resource.
- **`resource`**: List of bare lowercase-kebab-case filenames without `.md` (e.g., `["homelab-operations-reference"]`); the note-to-resource relationship property. A direct `project` or `area` value on a note is optional supplementary metadata only when useful for filtering or discovery.

## Agent Skill Frontmatter

`agents/skills/<skill-name>/SKILL.md` is a documented exception to the ordinary vault-note schema. It must contain `name`, `description`, and `status`, plus exactly one `tags` value of `skills/<skill-name>`. The `name` and tag suffix must exactly match the skill folder name. Agent Skills do not require `kind` or `created`; this avoids retrofitting invented metadata into imported third-party skills.

## Naming Patterns

| Pattern | Kind | Example |
|---------|------|--------|
| `area-name` | `kind: area` | `homelab.md` |
| `project-name` | `kind: project` | `homelab-documentation-baseline.md` |
| `resource-name` | `kind: resource` | `homelab-operations-reference.md` |
| `subject-name` | `kind: note` | `proxmox-nfs-settings.md` |
| `diagram-type-diagram` | `kind: note, type: diagram` | `service-interaction-sequence-diagram.md` |

## Naming Rules

- Use lowercase kebab-case for all filenames and folder names
- Prefer specific subjects over generic names (`network-storage-overview.md` vs `notes.md`)
- Use singular nouns for single items, plural for collections
- Avoid dates, versions, and status words in filenames; use `status` in frontmatter instead
- Reserve `AGENTS.md`, `INDEX.md`, `README.md`, and `SKILL.md` for their established purposes

## Routing Content

Place content in the folder whose primary role matches the note's purpose:

| Content Type | Primary Folder | Reason |
|--------------|----------------|---------|
| Daily entries | `journals/days/` | Time-bound, chronological capture |
| Ongoing responsibilities | `areas/` | Continuous work without deadline |
| Finite projects | `projects/` | Defined start/end with measurable outcome |
| Reference material | `resources/` | Persistent, reusable knowledge |
| Atomic ideas | `notes/` | Self-contained, reusable concepts |
| Visual maps | `canvases/` | Spatial arrangements requiring layout |
| Supporting assets | `files/` | Non-notes (images, docs, scripts) |
| Structural plans | `plans/` | Future-oriented, reviewable work |
| Reusable templates | `templates/` | Shared structures for new content |

## Status Flow

- `active` → `paused` → `complete` → `archive`
- `complete` remains visible; `paused` indicates deferred work
- `archive` excludes content from active dashboards and Base views
