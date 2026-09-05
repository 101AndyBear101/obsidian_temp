# Vault Naming Guidance

Use predictable, descriptive names so notes remain easy to find, link, embed, and query in Obsidian.

## General Rules

- Use lowercase kebab-case for ordinary folders and files: `proxmox-nfs-settings.md`.
- Prefer a specific subject over generic names such as `notes.md`, `new-note.md`, or `test.md`.
- Put the most important subject first, then its qualifier or type: `network-storage-overview.md`, `service-interaction-sequence-diagram.md`.
- Use singular nouns for one thing and plural nouns only for collections.
- Avoid dates, versions, and status words in a filename unless they identify the note itself. Put ordinary status in frontmatter instead.
- Keep names stable after other notes link to or embed them. Plan and verify link updates before renaming an existing file.

## Reserved Names

Use these exact capitalized names only for their established purposes:

- `AGENTS.md` — instructions for agents working in the vault.
- `INDEX.md` — a navigational index for a folder or collection.
- `README.md` — usage or maintenance guidance for a folder.
- `SKILL.md` — the required instruction file inside an Agent Skill folder.

## Folder Names

- Keep the root role-based folders stable: `bases`, `journals`, `areas`, `projects`, `resources`, `notes`, `canvases`, `files`, `plans`, and `templates`.
- Use lowercase kebab-case for new subfolders: `server-guides`, `project-plans`, `plantuml-diagrams`.
- Do not rename existing folders merely to change style; create a plan first when a rename affects links, embeds, Bases, or templates.

## Note Types

See [[CONVENTIONS#Naming Patterns]] for the full table of note type naming patterns and examples.

## Metadata Values

See [[CONVENTIONS#Metadata Schema]] for the canonical rules.

Key rules:
- Use lowercase kebab-case for `kind`, `status`, and `type` values.
- Use compact lowercase identifiers for `area`, `project`, and `resource` values; allow letters, numbers, hyphens, and underscores without spaces.
- Use ISO dates: `YYYY-MM-DD`.

## Before Creating or Renaming

1. Check for an existing note with the same subject.
2. Select the matching note-type pattern above.
3. Confirm the name will remain accurate as the content grows.
4. For existing notes, check inbound links and embeds before changing the filename or an embeddable heading.
