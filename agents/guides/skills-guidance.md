# Skills Guidance

Agent Skills capture reusable, vault-specific workflows. Store each skill under `agents/skills/<skill-name>/SKILL.md`.

## Core Workflows

- Create, update, standardize, or evaluate a skill with [[agents/skills/skill-authoring/SKILL|skill-authoring]].
- Import, audit, or normalize skills with [[agents/skills/skill-ingestion/SKILL|skill-ingestion]].
- Create or troubleshoot dynamic templates with [[agents/skills/templater-obsidian/SKILL|templater-obsidian]].

## Specialized Skills

- Use [[agents/skills/plantuml-obsidian/SKILL|plantuml-obsidian]] for PlantUML rendering via the joethei PlantUML plugin.
- Use [[agents/skills/plantuml-diagrams/SKILL|plantuml-diagrams]] for PlantUML source.
- Use [[agents/skills/mermaid-diagrams/SKILL|mermaid-diagrams]] for Mermaid source.

## Skill Standards

- Keep one focused capability per skill.
- Agent Skills are an exception to ordinary vault-note frontmatter: require `name`, `description`, `status`, and exactly one `skills/<skill-name>` tag; do not require `kind` or `created`. See [[CONVENTIONS#Agent Skill Frontmatter]].
- Add the skill to `agents/skills/INDEX.md` and run the skills audit after creating or materially changing it.
- Do not create a skill for an individual project decision; capture that in `plans/` or the relevant project note.
