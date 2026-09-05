# Obsidian Template Vault — Agent Instructions

## Workflow

- Follow [[agents/guides/workflow-guidance#Planning Mode]] before making changes.
- Read [[agents/guides/workflow-guidance#Post-Edit Validation]] before editing any note.
- Treat planning as read-only until implementation is explicitly requested.
- Create a reviewable note in `plans/` before broad structural or cross-vault changes.
- Make focused changes in small, verifiable batches.
- Run `python agents/validators/master.py --validation_path .` at the start and end of a chat session to validate vault consistency (ask before running).
- See [[agents/guides/workflow-guidance]] for vault principles, ingest guidelines, and atomic note authoring guidance.

## Internal Prompt Blocks

> When completing a template that contains an `internal_prompt` fenced code block, follow this workflow:

1. Read the entire template before asking questions or making edits.
2. Identify every `internal_prompt` block and its questions.
3. Ask only the clarifying questions needed to answer all prompts, following each block’s numbered order.
4. After the user responds, write the completed response immediately after each prompt block’s closing fence; never write inside a prompt block.
5. Keep the blocks until every prompt has a completed response.
6. Run `python agents/scripts/remove_internal_prompts/remove_internal_prompts.py <note-path>` to remove the completed prompt blocks while retaining the responses.
7. Read the completed note and verify that all responses remain and no `internal_prompt` blocks remain.
8. Do not run the cleanup script on a reusable template unless the user explicitly asks to remove its prompts.

## Vault Structure

- Use `bases/` for views and `journals/` for time-based capture.
- Organize knowledge as `areas/` → `projects/` → `resources/` → `notes/`.
- Use `canvases/` for visual maps and `files/` for attachments.
- Use `plans/` for proposed work and `templates/` for reusable note structures.
- Keep agent guidance in `agents/guides/` and reusable workflows in `agents/skills/`.
- See [[agents/guides/organization-guidance]] for detailed folder responsibilities and relationships.

## Note Model Guidance

- Keep canonical information in focused atomic notes.
- Build contextual wiki notes with Obsidian links and embeds instead of duplicating source content.
- Use stable headings when other notes embed specific sections.
- Never store secrets or sensitive credentials in the vault.
- Link or embed instead of copying content between notes.
- See [[agents/guides/note-model-guidance]] for the complete model.

## Naming Guidance

- Use descriptive, lowercase kebab-case names for folders and ordinary files.
- Prefer names that remain clear when viewed outside their parent folder.
- Keep headings used by embeds stable and descriptive.
- Preserve reserved filenames such as `AGENTS.md`, `README.md`, `INDEX.md`, and `SKILL.md`.
- Use compact lowercase identifiers for `area`, `project`, and `resource` metadata values; hyphens and underscores are allowed.
- See [[agents/guides/naming-guidance]] for the full naming rules.

## Organization Guidance

- Include the standard metadata fields `kind`, `status`, and `created` where applicable.
- Store `area` as a single plain filename and `project` or `resource` as lists of plain filenames.
- Use Obsidian wikilinks in note bodies for navigation and embeds.
- Keep archived material in its role folder with `status: archive`.
- Follow the PARA hierarchy: area → projects → resources → notes.
- See [[agents/guides/organization-guidance]] for schemas and relationship rules.

## Skills Guidance

- Check [[agents/skills/INDEX|Agent Skills Index]] for a workflow that matches the task.
- Read the selected skill's `SKILL.md` completely before using it.
- Use the narrowest applicable workflow and follow its validation steps.
- Add or update index and audit entries when creating or changing vault-local skills.
- Keep one focused capability per skill with a unique `skills/<skill-name>` tag.
- See [[agents/guides/skills-guidance]] for skill governance.

### Most Used Obsidian Skills

- [[agents/skills/defuddle/SKILL|defuddle]] — Extract readable Markdown from HTML pages.
- [[agents/skills/json-canvas/SKILL|json-canvas]] — Create and validate JSON Canvas files.
- [[agents/skills/obsidian-bases/SKILL|obsidian-bases]] — Create and edit Obsidian Base views.
- [[agents/skills/obsidian-cli/SKILL|obsidian-cli]] — Operate Obsidian through its CLI.
- [[agents/skills/obsidian-markdown/SKILL|obsidian-markdown]] — Author Obsidian Flavored Markdown.
- [[agents/skills/obsidian-templater/SKILL|obsidian-templater]] — Create and maintain Obsidian Templater templates.
