---
kind: plan
status: active
created: 2026-08-26
tags:
  - vault/maintenance
---

# Guidance Adjustment Plan

## Purpose

Align the guidance layer for clarity, conciseness, and reduced redundancy — without changing the vault's rules or conventions.

## End State

After implementation, the guidance layer will have three tiers:

```
README.md              → Human onboarding (what is this vault, how to start)
                         links to CONVENTIONS.md for reference

CONVENTIONS.md         → Human reference for folder roles, schema, naming, routing
                         (new file — single source of truth for all conventions)

AGENTS.md              → Agent quick-reference (~8 deferral bullets, all linking to guides)

agents/guides/
├── workflow-guidance.md  → Vault Principles, planning mode, implementation mode,
│                           post-edit validation
│                           (merged from working-mode + before-editing + purpose)
├── organization-guidance.md  → Root structure, routing, PARA, metadata, subfolders (as-is)
├── note-model-guidance.md    → Atomic vs contextual notes, sensitive content (as-is)
├── naming-guidance.md        → File naming, metadata values (as-is, with one fix)
└── skills-guidance.md        → Skill governance (as-is, with one fix)
```

Files removed: (none — all content preserved in merged files)

---

## Strategic Phases

### Phase 1 — Foundation: Schema and Conventions

**Why first**: Establishes the single source of truth. Everything else references this.

**Deliverable**: `CONVENTIONS.md` at vault root.

**Content**:
- Folder roles table (from README, de-duplicate)
- Full metadata schema (core, relationship, semantic properties)
- Kind-specific required vs optional properties table
- Routing Content table (from organization-guidance, reference only)
- Note type naming patterns table (from naming-guidance, reference only — CONVENTIONS.md is the canonical source; other files link to it rather than maintaining their own copies)

**Precision rules**:
- `CONVENTIONS.md` is the canonical source for schema, naming, and routing tables.
- `agents/guides/organization-guidance.md` and `naming-guidance.md` replace their local schema/naming tables with wikilinks to `CONVENTIONS.md`.
- `README.md` removes its Folder Guide table (replaced by a link to `CONVENTIONS.md`).
- Agent workflow instructions (planning mode, editing steps, skill governance) stay in `agents/guides/` — never duplicated in CONVENTIONS.

**Files affected**:
- `CONVENTIONS.md` (new)
- `README.md` (remove Folder Guide table, add link to CONVENTIONS.md)
- `agents/guides/organization-guidance.md` (remove Routing Content and Standard Properties tables, add wikilink to CONVENTIONS.md)
- `agents/guides/naming-guidance.md` (remove Note Types and Metadata Values tables, add wikilink to CONVENTIONS.md)

---

### Phase 2 — Consolidate: Remove Redundant Guidance

**Why second**: Eliminate duplication and simplify the file tree before trimming AGENTS.md.

**Actions**:

| Action | Rationale |
|---|---|
| Merge `working-mode-guidance.md` + `before-editing-guidance.md` + `vault-purpose-guidance.md` → `workflow-guidance.md` | All describe how to work in the vault — purpose sets the principles, working-mode and before-editing define the process |
| Rename `vault-local-skills-guidance.md` → `skills-guidance.md` | Shorter, consistent prefix with other guidance files |

**Merged `workflow-guidance.md` structure**:
- Vault Principles (from vault-purpose-guidance)
- Planning Mode (from working-mode-guidance)
- Implementation Mode (from working-mode-guidance)
- Post-Edit Validation (from before-editing-guidance)
- Scope Boundaries (from working-mode-guidance)

No rules change — only consolidation.

**Fixes applied during merge**:
- Remove "Keep sensitive information out of notes and plans" from Scope Boundaries (defer to `note-model-guidance.md#Sensitive Content`)
- Remove "run the skills audit" dangling reference (defer to `skills-guidance.md`)

**Files affected**: 6 files (merge 3 into 1, rename 1, update 2 inbound wikilinks in AGENTS.md and vault-local-skills-guidance.md).

**Rollback strategy**: Before executing Phase 2, copy the 3 source files to a `plans/_backups/` directory. If any wikilink breaks, restore from backup and adjust.

**Note**: README's opening paragraph already captures the vault purpose independently. No changes needed there.

---

### Phase 3 — Tighten AGENTS.md

**Why third**: Only after the guides are clean and files are named correctly.

**Principle**: One summary bullet + one deferral link per section. No inline repetition of guidance content.

**Before → After per section**:

| Section | Current | Target |
|---|---|---|
| Purpose | 3 bullets | 2 bullets: "See [[agents/guides/workflow-guidance#Vault Principles]] for vault purpose." (keep summary, defer details) |
| Current Working Mode | 4 bullets | 1 bullet: "Follow [[agents/guides/workflow-guidance#Planning Mode]] before making changes." |
| Vault Structure | 6 bullets | 4 bullets (trim description-style bullets, keep routing logic) |
| Note Model | 5 bullets | 2 bullets: summary + "See [[agents/guides/note-model-guidance]]." |
| Naming Guidance | 5 bullets | 2 bullets: summary + "See [[agents/guides/naming-guidance]]." |
| Organization Guidance | 5 bullets | 2 bullets: summary + "See [[agents/guides/organization-guidance]]." |
| Before Editing | 6 bullets | 2 bullets: "Read [[agents/guides/workflow-guidance#Post-Edit Validation]] before editing." |
| Vault-Local Skills | 4 bullets + skill list | 2 bullets + skill list (keep skill list, trim governance deferral) |

**Result**: AGENTS.md shrinks from ~73 lines to ~30 lines while preserving all navigation value.

**Files affected**: `AGENTS.md` (update all deferral wikilinks to match renamed guidance files).

**Rollback strategy**: `plans/_backups/AGENTS.md` backup created in Phase 2 covers this.

---

### Phase 4 — Fix: Naming Ambiguity

**Why fourth**: Small targeted fix on `naming-guidance.md`.

**File**: `agents/guides/naming-guidance.md`

**Change**: Metadata Values section

| Current | Target |
|---|---|
| "Use lowercase kebab-case for controlled values such as `kind`, `status`, `area`, `project`, `resource`, and `type`." | "Use lowercase kebab-case for `kind`, `status`, and `type` values. Use plain lowercase-kebab-case filenames for `area`, `project`, and `resource` values." |

**Files affected**:`agents/guides/naming-guidance.md`

---

### Phase 5 — Author: Content Creation Guidelines

**Why fifth**: These are new content — they depend on the schema (Phase 1) and workflow (Phase 2) being finalized.

**Destination**: Both go into `agents/guides/workflow-guidance.md` as new subsections after Post-Edit Validation.

**#### 5a. Ingest Guidelines**

Decision tree:
1. Does this content belong in the vault?
2. Does a note already exist?
3. What `kind` does it become?

Workflow: Capture → Classify → Normalize → Link → Validate

With template for ingested external notes:
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

**#### 5b. Atomic Note Authoring Guidelines**

Structure: Purpose → Settings/Procedure → Validation → Related

Guidelines for scope, headings stability, content quality, metadata, and linking.

With template:
```yaml
---
kind: note
status: active
type: permanent
created: YYYY-MM-DD
resource:
  - parent-resource-name
tags:
  - topic/area
---

# Canonical Subject

## Purpose

One sentence explaining what this note owns.

## Settings or Procedure

Canonical values or steps. Use stable `##` headings for embeddable content.

## Validation

How to verify correctness.

## Related

- [[resources/parent-resource-name|Parent resource]]
- [[notes/related-note|Related note]]
```

**Files affected**: `agents/guides/workflow-guidance.md`

---

### Phase 6 — Polish: Base Template Titles

**Why last**: Independent of all guidance changes, but fixes a usability issue.

**Files**: 
- `templates/base/area-template.md`
- `templates/base/notes-template.md`
- `templates/base/projects-template.md`
- `templates/base/resources-template.md`
- `templates/base/daily-template.md`

**Problem**: Each uses a diagram-type name as its placeholder title (e.g. `# activity-diagram` in area-template).

| Template | Current title | Target title |
|---|---|---|
| area-template.md | `# activity-diagram` | `# area-name` |
| notes-template.md | `# archimate-diagram` | `# note-title` |
| projects-template.md | `# class-diagram` | `# project-name` |
| resources-template.md | `# deployment-diagram` | `# resource-name` |
| daily-template.md | `# skill-template` | `# YYYY-MM-DD` |

Also update Base filters inside templates that reference the old placeholder name (e.g. `area == "activity-diagram"` → `area == "area-name"`).

**Files affected**: 5 template files.

---

## Dependency Graph

```
Phase 1 (schema)
  └─► Phase 2 (consolidate) ──► Phase 3 (AGENTS.md)
                                    └─► Phase 4 (naming fix)
  └─► Phase 5 (guidelines) ──► Phase 6 (templates)
```

Phases 1-4 are prerequisites for 5. Phase 6 is independent and can be done any time.

## Priority

| Phase | Effort | Impact | Dependency |
|---|---|---|---|
| 1 — Schema and Conventions | Medium | High | None (start here) |
| 2 — Consolidate Guidance | Medium | High | Requires Phase 1 |
| 3 — Tighten AGENTS.md | Small | Medium | Requires Phase 2 |
| 4 — Naming Ambiguity Fix | Tiny | Low | Requires Phase 2 (file rename) |
| 5 — Content Guidelines | Medium | Medium | Requires Phases 1, 2 |
| 6 — Template Titles | Small | Medium | Independent |

## Validation

1. `CONVENTIONS.md` schema matches all existing vault frontmatter — no contradictions.
2. All wikilinks in guidance files resolve after renames and deletions.
3. No file in `agents/guides/` duplicates a rule stated in `CONVENTIONS.md` or vice versa.
4. AGENTS.md has no bullet that repeats content from a guide file.
5. Sensitive content rules appear only in `note-model-guidance.md` — all other files defer.
6. The dangling "run the skills audit" reference is gone.
7. `CONVENTIONS.md` replaces the folder table in README and the schema tables in organization/naming guidance — no duplicates remain.
8. Base template titles match their intended purpose and filters are updated.

## Validation Results

| Check | Status | Notes |
|---|---|---|
| CONVENTIONS.md schema matches vault frontmatter | ✅ Pass | Verified against area, project, resource, note, and daily templates |
| No broken wikilinks in guidance layer | ✅ Pass | Grep confirms no references to deleted files (`before-editing-guidance`, `working-mode-guidance`, `vault-purpose-guidance`, `vault-local-skills-guidance`) |
| CONVENTIONS.md is the single source of truth | ✅ Pass | Schema and naming tables removed from organization-guidance and naming-guidance — both link to CONVENTIONS |
| AGENTS.md has no inline repetition of guidance | ✅ Pass | All sections defer to guides via wikilinks |
| Sensitive content in one place only | ✅ Pass | Only `note-model-guidance.md` contains sensitive content rules |
| Base template titles match purpose | ✅ Pass | `area-name`, `note-title`, `project-name`, `resource-name`, `YYYY-MM-DD` |
| Template area filters updated | ✅ Pass | `area == "area-name"` in area-template, `project.contains("project-name")` in projects-template, `resource.contains("resource-name")` in resources-template |
| No dangling "run the skills audit" reference | ✅ Pass | Removed during merge — only present in skill-template as intended |

## Progress

- [x] Phase 1 — Create CONVENTIONS.md with schema and conventions
- [x] Phase 2 — Consolidate guidance: merge working-mode + before-editing + vault-purpose into workflow-guidance.md; rename vault-local-skills-guidance → skills-guidance
- [x] Phase 3 — Tighten AGENTS.md to deferral-only quick-reference
- [x] Phase 4 — Fix naming ambiguity in `naming-guidance.md`
- [x] Phase 5 — Add ingest and atomic note guidelines to `workflow-guidance.md`
- [x] Phase 6 — Fix base template placeholder titles