# Vault Organization Guidance

Use folders to express a note's primary purpose, metadata to express its lifecycle and relationships, and links to create navigable context. Bases provide views over the structure; they are not additional storage locations.

## Organization Model

- Every note has one clear canonical location.
- A note's folder answers **what role does this content serve?**
- Metadata answers **what is its state and what does it relate to?**
- Wikilinks and embeds answer **where is this useful?**
- Archived content stays in its canonical folder with `status: archive`; the vault does not use a separate archive folder.

## Root Structure

```text
vault/
├── bases/          dashboards and queryable Base views
├── journals/       time-oriented capture and review
│   ├── days/       daily notes named YYYY-MM-DD.md
│   └── years/      optional annual indexes and reviews
├── areas/          ongoing responsibilities without an end date
├── projects/       finite efforts with a defined outcome
├── resources/      reusable collections of related reference notes
├── notes/          atomic source notes and contextual wiki notes
├── canvases/       spatial maps and visual working surfaces
├── files/          attachments and supporting non-note files
├── plans/          reviewable plans for structural changes
├── templates/      reusable note and diagram templates
└── agents/
    ├── guides/     vault-wide instructions and conventions
    └── skills/     reusable agent workflows
```

The role-based root folders are stable. Do not add, remove, or rename them without a reviewable plan in `plans/`.

## Routing Content

Use the [[CONVENTIONS#Routing Content|routing table in CONVENTIONS]] to find the right folder for new content.

## PARA Relationships

The vault's optional logical hierarchy is:

```text
area
└── multiple projects
    └── multiple resources
        └── multiple notes
```

Represent this hierarchy with metadata rather than nested folders:

- A project may identify a related area through the scalar `area` property using a compact lowercase identifier.
- A resource may identify one or more related projects through the `project` list property using compact lowercase identifiers.
- A note may identify one or more related resources through the `resource` list property using compact lowercase identifiers.
- A note may also identify related projects or an area as optional supplementary metadata when that direct relationship improves filtering or discovery.

Relationship properties are optional; use them when they provide useful context. The list properties allow a resource or note to be reused in more than one context without duplication. Projects do not own private copies of resources or notes; all content remains canonical in its role-based root folder and connects through metadata plus ordinary wikilinks.

## Standard Properties

Use `kind`, `status`, and `created` for notes that participate in organized views. Add relationship properties and `type` only when they describe the note.

See [[CONVENTIONS#Metadata Schema]] for the complete schema including core properties, relationships, semantic properties, and kind-specific requirements.

## Relationships and Lifecycle

- Store `area`, `project`, and `resource` values as compact lowercase identifiers (e.g. `home_ops`). Allow letters, numbers, hyphens, and underscores without spaces; values do not need to resolve to filenames.
- Use ordinary wikilinks in note content for navigation and context.
- `archive` is the only status excluded from active dashboard and Base views. Use `complete` for finished work that should remain visible and `paused` for work intentionally deferred.
- Daily notes live in `journals/daily/`, use `kind: note` and `type: journal`, and are surfaced by the journals dashboard and Base view.

The normal lifecycle is `active` → `paused` or `complete` → `archive`. A note may return to `active` when its work resumes. Changing status does not require moving the file.

Use lowercase kebab-case for controlled values and ISO dates (`YYYY-MM-DD`). Follow [[naming-guidance|Vault Naming Guidance]] for tag and file naming.

## Subfolder Policy

- Keep notes directly in their root category until a durable collection genuinely improves navigation.
- Name new subfolders in lowercase kebab-case and give each one a single documented purpose.
- Do not create matching area, project, and resource directory trees; metadata already represents those relationships.
- Keep diagrams with their reusable templates in `templates/` and finished visual work in `canvases/` or the relevant canonical note.
- Plan any subfolder rename that affects links, embeds, templates, Bases, or settings before implementation.

## Change Discipline

- Make small batches of changes that can be reviewed and reverted easily.
- After changing a filename, location, heading used for embeds, or metadata, verify affected links, embeds, and Base views.
