---
name: skill-authoring
status: active
description: Create, standardize, and evaluate vault-local Agent Skills.
tags:
  - skills/skill-authoring
---

# Vault Skill Authoring

## Outcome

Create a small, focused, and valid Agent Skill that captures non-obvious vault-specific workflow knowledge without adding unnecessary instructions or files.

## Required Structure

Each skill lives in `agents/skills/<skill-name>/` and must contain:

```text
<skill-name>/
└── SKILL.md
```

Optional directories are permitted only when they serve a concrete purpose:

- `scripts/` — deterministic, reusable automation.
- `references/` — detailed material that is only needed for particular modes or edge cases.
- `assets/` — templates or other files that belong in generated output.
- `agents/openai.yaml` — optional Codex UI metadata.

Do not create placeholder directories, README files, sample files, or scripts merely to make a skill look complete.

## Create or Update Workflow

1. Define one specific capability and its activation boundary. If it would cover unrelated workflows, split it into separate skills.
2. Start from [[templates/base/skill-template|the skill template]], then choose a lowercase, hyphenated name of 1–64 characters. The folder name and frontmatter `name` must match exactly; do not use leading/trailing or consecutive hyphens.
3. Write `SKILL.md` with YAML frontmatter and concise Markdown instructions.
4. Write a concise imperative description that says when to use the skill and reflects the user's intent, not its internal implementation. Include discriminating contexts and boundaries; avoid vague claims such as “helps with notes.”
5. Keep the main instructions focused on decisions, constraints, and workflow. Do not repeat general agent behavior or policy already provided by the environment.
6. Use progressive disclosure: move substantial conditional details to a directly linked, focused reference file. Keep file references relative to the skill root and no deeper than one reference hop.
7. Add scripts only when repeated logic benefits from reliable execution. Document dependencies and error behavior, then run the script against safe test input.
8. Validate the completed skill before handoff.

## Evaluation and Iteration

For a new or materially changed skill, begin with 2–3 realistic tasks before investing in a large test suite. Include at least one edge case or near miss.

- Compare the result with the skill against a no-skill or previous-version baseline when practical.
- Define observable assertions after inspecting the first outputs; avoid brittle wording-only checks.
- Keep a human review step for usefulness and fit.
- Revise from repeated failure patterns or actual user corrections, then rerun the same tests in a new iteration.
- Add a bundled script only when repeated execution proves that deterministic logic improves the result.

For description tuning, use both should-trigger and should-not-trigger prompts. Test near-misses rather than obviously unrelated prompts, and broaden or narrow concepts—not individual failed keywords.

## SKILL.md Minimum

```yaml
---
name: skill-name
description: Explain the focused capability and when an agent should use this skill.
status: active
tags:
  - skills/skill-name
---
```

The body should explain the desired outcome, essential workflow, non-obvious constraints, and when to load any supporting resources.

Optional frontmatter is allowed only when it adds value:

- `license` for a clear licensing statement.
- `compatibility` only when the skill requires a particular environment, package, network access, or product.
- `metadata` for simple string properties such as author or version.
- `allowed-tools` only when the target agent supports and needs the experimental restriction.

For this Obsidian vault, Agent Skills are an exception to ordinary note frontmatter. Use [[templates/base/skill-template|skill-template.md]] and require `name`, `description`, `status`, and exactly one tag in the form `skills/<skill-name>`; do not add `kind` or `created`. When normalizing an existing skill, preserve its purpose, licenses, and attribution.

## Vault-Specific Rules

- Keep planning-only skills read-only unless the user explicitly authorizes implementation.
- Preserve Obsidian links, embeds, metadata conventions, and sensitive-information safeguards.
- Put reusable vault methods in skills; put an individual project’s decisions and checklist in `plans/` instead.
- Before changing an existing skill, read its complete `SKILL.md` and every directly referenced resource that applies to the requested change.

## Validation

Run the bundled validator after creating or materially changing a skill:

```powershell
& '<python-path>' '<skill-creator-path>\scripts\quick_validate.py' '<path-to-skill>'
```

Also confirm manually:

- The frontmatter is valid and `name` matches the folder.
- The description is specific enough for correct activation.
- The instructions preserve user authorization boundaries.
- Every referenced file exists and is directly linked from the appropriate instructions.
- No unfinished placeholders remain.

For scripts, also require non-interactive input, `--help`, clear errors, structured stdout when data is consumed downstream, and safe/dry-run behavior for stateful work.

## References

This skill follows the Agent Skills open specification: <https://agentskills.io/specification>.
