---
kind: plan
status: complete
created: 2026-08-26
tags:
  - vault/maintenance
  - vault/quality
---

# Vault Quality Improvement Plan

## Goal

Bring reusable templates, metadata guidance, Agent Skill conventions, and static validation into a consistent, enforceable state without changing the vault structure or breaking existing links.

## Task for Sol

Implement and verify this plan. Correct reusable base-template frontmatter and creation dates; reconcile metadata documentation; define and enforce the Agent Skill frontmatter contract; and expand static validation coverage. If earlier work already exists, first verify it against this plan's acceptance criteria and change only remaining defects.

## Constraints

- Preserve the existing vault structure, links, embeds, Base filters, and third-party skill licenses and attribution.
- Do not rename `templates/mermaid_diagrams/` or `templates/plantuml_diagrams/`.
- Do not change the PARA folder structure.
- Do not move the vault into the WSL filesystem.
- Do not rewrite imported third-party skill content beyond explicitly approved metadata normalization.
- Follow [[agents/guides/workflow-guidance#Post-Edit Validation]] after every edit batch.
- Ask before running `python agents/scripts/master_validation.py` unless the user has already explicitly authorized that run.

## Acceptance Criteria

1. Every base template has valid YAML frontmatter.
2. Base templates use valid Templater expressions rather than a fixed historical creation date.
3. A daily note derives its title and `created` value from its note date where appropriate.
4. Base-template headings, relationship placeholders, and Base filters remain correct.
5. Documentation consistently uses `tags`, scalar `area`, and list `project` and `resource` properties.
6. Documentation clearly defines `resource` as the note-to-resource relationship property.
7. Agent Skills have a documented exception contract requiring `name`, `description`, `status`, and exactly one matching `skills/<skill-name>` tag.
8. The skill template and ingestion audit enforce that contract without changing third-party licenses or attribution.
9. Static validation detects malformed base-template frontmatter and invalid diagram-template fences or languages.
10. `python agents/scripts/master_validation.py` passes in the configured Zed WSL sandbox.

## Material Risks

- Templater syntax is plugin-dependent and should be rendered in Obsidian before becoming canonical.
- Stronger validation can expose intentional legacy exceptions; record them explicitly rather than weakening validators.
- Changes to schema wording can contradict existing examples or Base filters if not reviewed together.
- A directory rename would be cross-vault structural work and is deliberately excluded.

## Work Breakdown

### Phase 1 — Inspect and Plan

- Inventory current template, guidance, skill, and validation behavior.
- Identify whether prior implementation already satisfies any acceptance criteria.
- Produce a brief implementation plan with file-level scope and risks.

### Phase 2 — Templates and Metadata Guidance

**Likely files:**

- `templates/base/area-template.md`
- `templates/base/daily-template.md`
- `templates/base/diagram-template.md`
- `templates/base/notes-template.md`
- `templates/base/projects-template.md`
- `templates/base/resources-template.md`
- `templates/base/skill-template.md`
- `CONVENTIONS.md`
- `AGENTS.md`
- relevant files in `agents/guides/`

**Required outcome:** Valid dynamic template frontmatter and unambiguous metadata documentation, with existing Base logic preserved.

### Phase 3 — Agent Skill Contract

**Likely files:**

- `templates/base/skill-template.md`
- `agents/guides/skills-guidance.md`
- `agents/skills/skill-ingestion/SKILL.md`
- `agents/skills/skill-ingestion/scripts/audit_skills.py`
- `CONVENTIONS.md`

**Required outcome:** A documented, mechanically checked Agent Skill exception contract compatible with the existing skills registry.

### Phase 4 — Static Validation and Verification

**Likely files:**

- `agents/scripts/frontmatter_validation.py`
- `agents/scripts/template_validation.py` or another narrowly scoped validator
- `agents/scripts/README.md`
- `agents/scripts/master_validation.py` only when a new validator requires registration

**Required outcome:** A validation path that catches malformed template frontmatter and invalid diagram-template fences/languages, is documented, and passes the full master suite.

## Required Parent-Orchestrated Workflow

The parent agent is the lead orchestrator and owns planning, architecture, direct delegation, review, and final synthesis. Do not require nested delegation or assume model-selection controls that the available runtime does not expose.

The parent agent must:

1. Define the goal, constraints, acceptance criteria, and material risks in a brief task plan.
2. Break work into small, non-overlapping direct leaf-agent tasks.
3. Delegate each task according to difficulty:
   - GPT-5.6 Luna for mechanical or high-volume work: file inventory, targeted search, extraction, summaries, log reduction, and explicitly specified test runs.
   - GPT-5.6 Terra for normal implementation, debugging, integration, focused investigation, and code review.
   - The parent agent for architecture, security or privacy, public interfaces, schema changes, irreversible actions, unresolved ambiguity, repeated failures, and review.
4. Do not use the parent agent for routine implementation when an approved direct leaf agent can perform it.
7. Give every leaf agent only this compact handoff:

   ```text
   Objective:
   Relevant inputs / files:
   Required output:
   Acceptance check:
   Response limit:
   ```

8. Require every leaf agent to return exactly:

   ```text
   Status: done | blocked
   Result: maximum 200 words
   Evidence: key findings, changed files, or commands only
   Risks: none or concise list
   Next action: one recommendation
   ```

9. Read returned summaries before requesting raw output. Request raw logs, full files, or further investigation only to resolve a failure or high-impact decision.
10. Use Luna to compress large outputs before forwarding them to Terra or reviewing them in the parent.
11. Avoid duplicate inspection and overlapping work.
12. Review each completed task against its acceptance check, issue narrow follow-ups when necessary, and stop once all acceptance criteria pass.
13. Return a concise final synthesis: completed work, verification evidence, remaining risks, and a direct-agent task ledger that records the assigned model.

The parent agent may bypass this workflow only to enforce safety, user approval, or a stated constraint.

## Deferred Decision

The underscore-named Mermaid and PlantUML template directories conflict with the vault's kebab-case guidance. Treat them as a documented compatibility exception unless a separately approved structural plan inventories and updates every affected link, template, setting, and Base query.

## Validation Record

| Check | Result |
| --- | --- |
| `python agents/scripts/master_validation.py` | 14 passed, 0 failed |
| `python agents/scripts/template_validation.py` | passed |
| `python agents/skills/skill-ingestion/scripts/audit_skills.py --skills-root agents/skills` | 11 skills valid; no issues or stale index entries |

No further edits were required because all plan acceptance criteria passed.

## Direct-Agent Task Ledger

| Task | Requested role | Outcome |
| --- | --- | --- |
| Validation inventory and specified test runs | Luna | Completed; full validation suite passed |
| Base-template review | Terra | Completed; all seven templates met criteria; no edits needed |
| Metadata, skill-contract, and validator review | Terra | Completed; criteria met; no edits needed |

The current runtime does not expose or verify an agent's exact underlying model. The requested Luna and Terra roles are recorded as task-routing instructions, not as independently verified model assignments.

## Remaining Risk

Templater expressions were statically validated but not rendered in a live Obsidian session. Confirm the generated frontmatter once for each base template before relying on it as canonical.
