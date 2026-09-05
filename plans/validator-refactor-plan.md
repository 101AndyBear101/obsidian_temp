---
kind: plan
status: complete
created: 2026-09-03
tags:
  - vault/validation
  - topic/python
---

# Validator Refactor Plan

## Objective

Refactor the vault validation suite into reusable, independently configurable validators with consistent command-line behavior, structured append-only logging, and colocated pytest coverage.

## Confirmed Requirements

- Give each validator one validation responsibility.
- Put each validator in its own folder with `<name>.py`, `ini_<name>.ini`, `test_<name>.py`, and `log_<name>.json`.
- Make every validator standalone, with no imports from other validation scripts.
- Use PyYAML for YAML frontmatter and pytest for tests; use the Python standard library for all other functionality where practical.
- Require `--validation_path` for every validator and the master runner. Do not provide configuration-path or output-path arguments.
- Accept either a file or directory as the validation path. Traverse directories recursively.
- Automatically load the validator's neighboring `ini_<name>.ini` when it exists.
- If an INI is missing, regenerate it from built-in defaults, record a warning, and continue.
- Treat a malformed INI or an unrecoverable configuration or execution failure as exit code `2`.
- A direct validator run appends one complete run object to its local `.jsonl` log.
- A master run writes each validator's local `log_<name>.json` and the combined `log_master.json`.
- Create a missing log without warning. Preserve malformed historical lines, append the current valid run, and report a warning about malformed history.
- Retain all log history for now. Do not rotate or trim logs.
- Use exit code `0` for clean or warning-only runs and `1` when validation errors exist.
- Validate every Markdown file unless an applicable INI ignore pattern excludes it. Do not hide file exceptions in validator code.

## Common Log Schema

Each JSON Lines line represents one complete run and uses the same versioned structure:

- `schema_version`
- `run_id`
- `validator`
- `started_at`
- `finished_at`
- `validation_path`
- `config_path`
- `files_checked`
- `issues`
- `summary`

Every issue contains `severity`, stable validator-specific `code`, `explanation`, `source_validator`, and `location`. Unused fields remain present with `null`; collections use empty arrays and real zero counts use `0`. Locations use validation-root-relative paths and one-based line and column numbers when available.

## Metadata Policy Changes

- Continue requiring `kind`, `status`, and `created` for ordinary notes.
- Recommend `type` for `kind: note` entries. A missing or empty type produces an actionable warning; an unsupported type or invalid data type is an error.
- Treat `tags` and kind-specific relationship fields as recommended where they may legitimately be absent; report actionable warnings instead of errors when they are missing or empty.
- Validate `area` as a scalar and `project` and `resource` as lists when present.
- Accept compact relationship identifiers containing lowercase letters, numbers, hyphens, and underscores, with no spaces. Warn when an identifier exceeds 20 characters.
- Do not require relationship identifiers to match filenames or resolve to files.
- Allow single-level and arbitrarily nested slash-separated tags. Each segment uses compact lowercase identifiers. Warn when the entire tag exceeds 30 characters.
- Keep malformed types and invalid identifier or tag syntax as errors.
- Preserve the separate Agent Skill frontmatter schema.
- Require `created` to use an exact `YYYY-MM-DD` value that represents a real calendar date. Do not warn solely because the date is in the future.
- Standardize daily journals under `journals/daily/`. Require daily filenames to use `YYYY-MM-DD.md` and treat them as an explicit exception to the general guidance against dates in filenames.
- Update `CONVENTIONS.md` and related guidance so documented rules match the implemented policy.

## Target Structure

Create `agents/validators/modular_validators/` with one subfolder per validator. Each folder contains a Python file matching its folder name, such as `bases/bases.py`. The master recursively discovers non-test Python files declaring `VALIDATOR_NAME` anywhere beneath its own directory. Missing validator scripts are simply absent from discovery and do not block the scripts that remain.

Each validator contains its own CLI, configuration loading, file discovery, parsing helpers, result model, exit-code handling, and log writer. The master executes each discovered validator as an independent Python process and aggregates the records written by those processes.

The `ini_master.ini` file beside `master.py` defines directories excluded from recursive script discovery and vault-wide validation ignores. The master builds a filtered validation directory and passes only that directory to each validator. Each local INI contains that validator's rules and any unique local ignore patterns. There is no required validator registry, so removing one validator does not prevent the master from running the others.

## Validator Boundaries

1. Frontmatter: YAML validity, required fields, types, controlled values, and kind-specific schemas.
2. Relationships: compact metadata relationship syntax and actionable missing-relationship recommendations; remove filename-resolution requirements.
3. Tags: tag syntax, hierarchy, configured patterns, and length warnings.
4. Wikilinks: target and heading resolution only; broken targets are errors.
5. Link coverage: inbound and outbound link recommendations; replace the overlapping orphan and inbound validators.
6. Naming: file and folder naming rules and configured exceptions.
7. Sections: configured structural expectations by kind and subtype.
8. Attachments: broken embeds and unreferenced attachments.
9. Indexes: index-specific content and resolution requirements not already owned by frontmatter or wikilinks.
10. Templates: Templater placeholders and diagram-fence validation, leaving shared frontmatter rules to the frontmatter validator.
11. Skills: skill-folder registration and layout, leaving skill frontmatter parsing to the frontmatter validator.
12. Bases: Base-view folder, property, and controlled-value references.
13. Duplicates: configurable filename-similarity recommendations.

## Implementation Sequence

1. Add PyYAML runtime requirements and pytest development requirements.
2. Embed result, issue, configuration, discovery, frontmatter, CLI, and JSON Lines logging utilities in every standalone validator.
3. Define and test default global and local INI generation.
4. Implement recursive master discovery, isolated subprocess execution, per-validator logging, and combined master logging.
5. Migrate frontmatter, relationship, and tag validators first because they establish the shared metadata model.
6. Replace orphan and inbound validators with link coverage, then migrate wikilinks.
7. Migrate remaining validators one at a time, removing duplicated discovery, parsing, reporting, and ignore logic.
8. Update documentation, commands, conventions, and ignore rules.
9. Remove the legacy scripts as part of the completed replacement. Do not retain compatibility wrappers or preserve the old command interface.

## Test and Acceptance Criteria

- Pytest discovers each colocated test module and the master tests.
- Every validator requires `--validation_path` and rejects missing or nonexistent paths with exit code `2`.
- File and directory validation paths work consistently.
- Master and local wildcard ignores use normalized vault-relative forward-slash paths.
- Missing INIs regenerate defaults and produce warnings; malformed INIs produce exit code `2` without overwriting user content.
- Direct runs append exactly one schema-valid JSON object to the local log.
- Master runs each standalone validator, appending one local record per validator and one combined object to the master log.
- `test_master.py` recursively discovers and runs every available `test_*.py` file except itself, continuing after failures.
- Missing logs are created; malformed historical lines are preserved and reported.
- Warning-only runs return `0`, validation errors return `1`, and execution failures return `2`.
- Summary counts equal the issues stored in each run record.
- Existing supported validation behavior remains covered or is documented as intentionally changed.

## Migration Safety

Implement and verify the replacement validator by validator, then remove the legacy scripts as part of the same refactor. Do not create compatibility wrappers or preserve the old command interface. Compare replacement results against representative vault fixtures before deleting legacy code. Do not bulk-edit vault content merely to make new validators pass; review findings separately.

## Validation

- Run focused pytest tests after each validator migration.
- Run the complete pytest suite after master-runner changes.
- Run the existing master validator before implementation and the replacement master validator after implementation, after receiving the required permission for each vault-wide validation run.
- Inspect generated INI defaults and JSON Lines records manually for schema and path correctness.
