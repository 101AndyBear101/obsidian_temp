# Workflow Guidance

## Vault Principles

This vault is a reusable template for a personal knowledge system organized with a PARA-style structure. It should demonstrate useful, portable patterns without carrying private or environment-specific operational content.

- Use realistic but non-sensitive examples; replace hostnames, addresses, accounts, and credentials with safe placeholders.
- Keep reusable structure and guidance, not one person's private history or active configuration.
- Preserve the role-based root folders because Bases, templates, and guidance may reference them.
- Put project-specific decisions in a plan or project note, not in global vault guidance.
- A new user should be able to copy this vault, understand where content belongs, and begin using it without removing private information or untangling personal-only conventions.

## Planning Mode

- Treat planning as read-only.
- Do not move, rename, split, delete, or overwrite notes.
- Inspect relevant notes, links, embeds, templates, and Bases before proposing a change.
- Create a reviewable Markdown plan in `plans/` before a broad structural change.
- State assumptions, scope, affected files, and validation steps in the plan.

## Implementation Mode

- Begin only after the user explicitly authorizes the change, or the request clearly asks for implementation.
- Work in small, reviewable batches.
- Preserve and update affected Obsidian links and embeds.
- Verify the result after each rename, move, or metadata change.

## Post-Edit Validation

Run this check after editing an existing note, especially after a move, rename, structural edit, or metadata change.

1. Read the relevant note in full.
2. Check its inbound and outbound links, embeds, and any headings used as embed targets.
3. Read [[naming-guidance|Vault Naming Guidance]] before creating or renaming content.
4. Check the applicable plan in `plans/`; create one first for broad structural work.
5. State the exact files that will change and keep the edit within that scope.
6. After editing, verify the changed note, related links and embeds, and any metadata-dependent Base views.

For planning-only requests, stop after inspection and the proposed plan. Do not make the edits until implementation is authorized.

## Scope Boundaries

- Do not infer permission to make a materially broader change than requested.
- Ask for direction when a missing decision would significantly change the vault structure or content.
- Follow [[note-model-guidance#Sensitive Content]] for handling sensitive information — do not duplicate those rules here.

## Ingest Guidelines

### Decision Tree

Before ingesting external content, ask:

1. **Does this content belong in the vault?**
   - Reference material, procedure, decision, or something reusable? → Yes
   - Temporary thought, chat log, or personal ephemera? → Journal or skip
   - Someone else's full work to reference rather than own? → Resource with `source` URL

2. **Does a note for this already exist?**
   - Search by subject, not filename. Update existing or add a heading instead of duplicating.

3. **What `kind` does it become?**
   - Reusable fact or procedure → `kind: note, type: permanent`
   - Daily journal entry → `kind: note, type: journal` in `journals/daily/`
   - External reference → `kind: resource` with `source` URL
   - Connecting existing notes → `kind: note, type: contextual`

### Workflow: Capture → Classify → Normalize → Link → Validate

**1. Capture**: Raw content goes into daily note or `inbox.canvas`. For web content, use the [[agents/skills/defuddle/SKILL|defuddle]] skill.

**2. Classify**: Determine `kind`, `type`, and target folder using the [[CONVENTIONS#Routing Content|routing table]].

**3. Normalize**:
- Add required frontmatter per the [[CONVENTIONS#Metadata Schema|schema]].
- Replace sensitive data with placeholders (`<server-address>`, `<api-token>`).
- Use lowercase kebab-case for filenames.
- Remove navigation, ads, boilerplate — keep only useful signal.

**4. Link**:
- Add relationship metadata (`area`, `project`, `resource`).
- Add wikilinks in the body to related notes.
- Add `source` URL if content came from an external origin.

**5. Validate**:
- Does the frontmatter match the schema for this `kind`?
- Do all wikilinks resolve?
- Are there any credentials, IPs, or real names that should be placeholders?
- Does the Base view for the parent resource/project include this note?

### What NOT to Ingest

- Full articles or documentation you can reference externally (use `source` instead)
- Credentials, tokens, private keys, personal contact details
- Ephemeral chat logs or conversations without extracted decisions
- Content that duplicates an existing note without adding new signal
- Anything that would require removing sensitive information before the vault can be shared

### Template for Ingested External Notes

```yaml
---
kind: note
status: active
type: permanent
created: YYYY-MM-DD
resource:
  - related-resource-name
source: https://example.com/original
tags:
  - topic/ingested
---
```

The `source` field preserves attribution. The `topic/ingested` tag marks externally sourced content for eventual cleanup traceability.

## Atomic Note Authoring Guidelines

### Structure

Every atomic source note should answer exactly one question or document exactly one procedure, configuration, definition, or decision.

```
# Title

## Overview

State what question this note answers or what procedure it owns — one sentence.

## Content

Canonical values or steps. Keep embeddable content under stable `##` headings.

## Related

Links and relationships to other notes (optional).
```

### Guidelines

**Scope**:
- One subject per note. If a note needs more than 3-4 top-level `##` sections, consider splitting.
- A note owns its subject; other notes link or embed from it rather than copy.

**Headings**:
- Use stable `##` headings for content that other notes should embed (`![[note#Heading]]`).
- Once a heading is embedded elsewhere, do not rename or delete it without updating all embed targets.
- Keep heading names descriptive and stable: `## Mount Options`, not `## Config`.

**Content**:
- Use examples with clear placeholders rather than abstract templates.
- List validation criteria explicitly so the reader knows when the procedure is complete.
- Add edge cases and failure modes when they are non-obvious.

**Metadata**:
- `kind: note`, `type: permanent`
- `resource` (optional, links upward in the PARA hierarchy)
- `tags` when useful for filtering (e.g. `homelab/documentation`)

**Linking**:
- Link to parent resource in both frontmatter (`resource`) and body when it provides context.
- Wikilinks in body content should point to canonical source notes, not duplicate their content.
- Use path-qualified links (`[[notes/note-name]]`) only when filenames repeat across folders.

### Template

```yaml
---
kind: note
status: active
type: permanent
created: YYYY-MM-DD
tags:
  - topic/area
---

# Title

## Overview

One sentence explaining what this note owns.

## Content

Document the canonical values or steps here. Keep embeddable content under stable `##` headings.

## Related

- [[notes/related-note|Related note]]
```

### What to Avoid

- Avoid generic titles like "Notes" or "Configuration" — name the file after the canonical subject.
- Avoid duplicating content from other notes — link or embed instead.
- Avoid storing credentials, tokens, or private configuration — use placeholders.
- Avoid long introductory paragraphs — the Purpose section should be one sentence.
- Avoid status or date in filenames — that belongs in frontmatter.