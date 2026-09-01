---
name: skill-ingestion
status: active
description: Import, audit, and normalize vault-local Agent Skills.
tags:
  - skills/skill-ingestion
---

# Skill Ingestion and Normalization

## Outcome

Bring an incoming skill into the vault without silently changing its intent: identify structural and registry gaps, propose minimal standards-aligned changes, then apply only approved conversions.

## Audit First

Run the audit from this skill directory, pointing it at the vault skill root:

```powershell
& '<python-path>' scripts/audit_skills.py --skills-root '<vault>/agents/skills'
```

The script writes a JSON report to stdout. It checks each immediate child skill folder and compares it with `INDEX.md` at the skill root.

Review these categories before changing files:

- Missing or malformed `SKILL.md` frontmatter.
- Invalid, absent, or mismatched `name`, `description`, `status`, or unique `skills/<skill-name>` tag fields.
- A skill missing from the index or an index entry with no skill folder.
- Unfinished scaffold placeholders.

## Conversion Workflow

1. Read the incoming skill completely, including each directly referenced resource that applies to its workflow.
2. Run the audit and write a conversion plan: source files, identified gaps, proposed changes, and checks.
3. Preserve the skill’s real purpose and constraints. For a new skill, start from [[templates/base/skill-template|skill-template.md]]; normalize existing skills only to the documented Agent Skill contract in [[CONVENTIONS#Agent Skill Frontmatter]] without inventing `kind` or `created` metadata.
4. Use `skill-authoring` and [[templates/base/skill-template|skill-template.md]] for naming, descriptions, frontmatter, progressive disclosure, scripts, and evaluation rules.
5. Do not delete source files or overwrite a skill in place without explicit approval. For a new incoming skill, change only its own folder and the skills index.
6. Validate structure after conversion, then update `INDEX.md` with the skill name, status, source, and a brief purpose.
7. Report both automated findings and the human judgment used for any non-mechanical rewrite.

## Index Rules

`INDEX.md` is the vault’s inventory, not the authority for a skill’s instructions. It must list every direct child skill folder containing `SKILL.md` and must not invent entries for missing folders.

Use one concise row per skill:

```markdown
| Skill | Status | Source | Purpose |
| --- | --- | --- | --- |
| `example-skill` | active | vault-local | Short purpose. |
```

## Guardrails

- Treat audit output as evidence, not permission to rewrite or delete.
- Keep the incoming skill’s licensing, attribution, and required resources unless the user explicitly authorizes a change.
- Do not import secrets, credentials, private keys, or user-specific data found in an incoming skill.
- Prefer a focused `SKILL.md`; move large conditional detail to directly linked references.
- Do not add scripts, assets, or placeholder folders unless the skill demonstrably needs them.
