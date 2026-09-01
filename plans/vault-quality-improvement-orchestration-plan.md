---
kind: plan
status: complete
created: 2026-08-26
tags:
  - vault/maintenance
  - vault/quality
  - agent-orchestration
---

# Vault Quality Improvement Orchestration Plan

## Context

This plan supersedes [[plans/vault-quality-improvement-plan|Vault Quality Improvement Plan]] as the execution guide. The earlier plan remains the record of its completed validation. This plan is for a future quality-improvement pass that uses parent-only orchestration.

## Goal

Bring reusable templates, metadata guidance, Agent Skill conventions, and static validation into a consistent, enforceable state while preserving vault structure, links, embeds, Base filters, licenses, and attribution.

## Architecture and Operating Rules

- The parent agent is the only orchestrator: it owns routing, dependencies, approvals, review, evidence collection, and final synthesis.
- Workers are direct leaf agents. They do not delegate, manage other agents, or make architectural decisions.
- Use Luna for bounded inventory, extraction, output compression, and specified test runs; use Terra for implementation, integration, and substantive review.
- Assign one writer to each file or feature. Parallel work is limited to non-overlapping files and responsibilities.
- Maintain the task ledger in this plan. Forward only its delta and a focused context capsule between tasks.
- Read worker summaries before asking for raw logs or full files.

## Constraints

- Preserve existing vault structure, links, embeds, Base filters, and third-party skill licenses and attribution.
- Do not rename `templates/mermaid_diagrams/` or `templates/plantuml_diagrams/`.
- Do not change the PARA folder structure or move the vault into the WSL filesystem.
- Do not rewrite imported third-party skill content beyond approved metadata normalization.
- Do not run `python agents/scripts/master_validation.py` until the parent obtains explicit user approval.

## Acceptance Criteria

1. Base templates have valid YAML frontmatter and dynamic Templater dates; daily notes derive their dates from the note date where appropriate.
2. Existing headings, relationship placeholders, Base filters, links, embeds, folder structure, and compatibility directory names remain intact.
3. Guidance consistently defines `tags`, scalar `area`, list `project`, and list `resource` properties.
4. Agent Skills require `name`, `description`, `status`, and exactly one matching `skills/<skill-name>` tag.
5. The skill audit enforces that contract without changing third-party licenses or attribution.
6. Static checks reject malformed base-template frontmatter and invalid diagram fences or languages.
7. Targeted checks pass; the master validation suite runs only after explicit approval.
8. Parent review finds no unresolved ownership conflicts, acceptance gaps, or unrecorded exceptions.

## Worker Handoff Contract

Every parent-to-worker handoff contains only:

```text
Task ID:
Objective:
Relevant inputs / files:
Required output:
Acceptance check:
Response limit:
Stop condition:
```

Every worker response contains exactly:

```text
Status: done | blocked
Result: maximum 200 words
Evidence: changed files, commands, or findings only
Risks: none or concise list
Next action: one recommendation
```

## Delegation Manifest

| ID | Objective | Dependencies | Worker | Effort | File ownership | Acceptance check | Response limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | Inventory compliance, prior work, exceptions, and exact edit scope; make no changes. | None | Luna | Low | None | Maps file-level findings to every criterion without duplicating inspection. | 200 words |
| T02 | Correct reusable templates while preserving behavior. | T01 | Terra | Medium | `templates/base/area-template.md`, `daily-template.md`, `diagram-template.md`, `notes-template.md`, `projects-template.md`, `resources-template.md` | YAML and Templater behavior are valid; headings, placeholders, and Base filters remain correct. | 200 words |
| T03 | Reconcile metadata guidance with the canonical schema and the skill exception defined by T04. | T01, T04 | Terra | Medium | `CONVENTIONS.md`, `AGENTS.md`, relevant guides except `agents/guides/skills-guidance.md` | Guidance agrees on metadata and defines `resource` unambiguously. | 200 words |
| T04 | Define and enforce the Agent Skill exception contract. | T01 | Terra | High | `templates/base/skill-template.md`, `agents/guides/skills-guidance.md`, `agents/skills/skill-ingestion/SKILL.md`, `agents/skills/skill-ingestion/scripts/audit_skills.py` | Template, documentation, and audit agree; tag match is exact; licenses and attribution remain unchanged. | 200 words |
| T05 | Expand and document narrowly scoped static validation. | T01, T02, T04 | Terra | High | `agents/scripts/frontmatter_validation.py`, selected template validator, `agents/scripts/README.md`, `agents/scripts/master_validation.py` only if registration is required | Targeted evidence proves malformed frontmatter and invalid diagram syntax are rejected without false failures. | 200 words |
| T06 | Run approved targeted validation and compress results; make no changes. | T02, T03, T04, T05 | Luna | Low | Relevant validators, skill audit, changed-file checks | Returns concise pass/fail evidence and exact failure command if needed; does not run master validation. | 150 words |
| T07 | Run the full master suite after explicit user approval. | T06, user approval | Terra | Medium | `agents/scripts/master_validation.py` in the configured Zed WSL sandbox | All checks pass, or the response contains only focused failure evidence and a narrow next step. | 200 words |

## Execution Order

```text
T01 inventory
  ├─ T02 templates ─┐
  └─ T04 skills ───┼─ T03 guidance
                   └─ T05 validators
                         ↓
                       T06 targeted validation
                         ↓
              explicit user approval required
                         ↓
                       T07 master validation
                         ↓
                   parent synthesis
```

T02 and T04 may run in parallel after T01 because their owned files do not overlap. T03 and T05 begin only after their dependencies finish. All remaining tasks are sequential.

## Risks and Escalation Conditions

- Escalate live Templater rendering or plugin-semantics questions to the parent; no worker should guess.
- Stop for approval before the master suite, structural changes, directory renames, schema expansion, or third-party content changes.
- Treat the Mermaid and PlantUML underscore directories as compatibility exceptions unless a separate approved structural plan covers every reference.
- Escalate overlapping edits, ambiguous canonical guidance, unexpected legacy exceptions, repeated validator failures, or any risk to links, embeds, Base filters, licenses, or attribution.

## Parent Task Ledger

| Task | Status | Assigned worker | Changed files | Verification evidence | Open risks |
| --- | --- | --- | --- | --- | --- |
| T01 | complete | Luna | — | Read-only inventory confirmed templates, metadata guidance, and skill-contract checks pass; identified the validator gap and plan-status defect. | None |
| T02 | complete | Terra | — | T01 confirmed the existing templates satisfy their acceptance check. | None |
| T03 | complete | Terra | — | T01 confirmed the existing metadata guidance satisfies its acceptance check. | None |
| T04 | complete | Terra | — | T01 confirmed the existing skill contract and audit satisfy their acceptance check. | None |
| T05 | complete | Terra | `agents/scripts/template_validation.py`, `agents/scripts/README.md`, `agents/scripts/duplicate_validation.py` | Added stateful Markdown-fence parsing and an unmatched-closing regression; tightened duplicate matching with plan-pair and normalized-duplicate regressions. | None |
| T06 | complete | Luna | — | `python agents/scripts/template_validation.py`, the skill audit, and `python agents/scripts/duplicate_validation.py` passed; master validation was not rerun. | None |
| T07 | complete | Terra | — | `python agents/scripts/master_validation.py`: 14 passed, 0 failed. | None |

## Completion Standard

The parent stops when every applicable acceptance criterion has passed, the ledger contains verification evidence, and remaining risks are non-blocking. The final report contains completed work, verification evidence, and concise remaining risks.
