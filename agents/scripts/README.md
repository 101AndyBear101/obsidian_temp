# Agent Maintenance Scripts

Utility scripts for vault maintenance tasks. Run from the vault root.

## Prerequisites

Python 3.8+ is required. All scripts use only the standard library.

## Scripts

| Script | Purpose |
|--------|---------|
| `frontmatter_validation.py` | Check all .md files against the CONVENTIONS schema (kind, status, type, created, required properties) |
| `wikilink_validation.py` | Find wikilinks that don't resolve to existing files or headings |
| `relationship_validation.py` | Validate area/project/resource metadata values point to existing files |
| `naming_validation.py` | Scan files/folders for lowercase-kebab-case compliance |
| `orphan_validation.py` | Find files with no inbound wikilinks from other notes |
| `index_validation.py` | Validate all INDEX.md files (frontmatter, wikilinks, resolution) |
| `skill_validation.py` | Check skills directory against INDEX.md registry for new/stale entries |
| `template_validation.py` | Validate base-template frontmatter, Templater date expressions, and Mermaid/PlantUML fence balance, unmatched closers, and languages |
| `attachment_validation.py` | Find unreferenced attachments and broken embeds |
| `base_validation.py` | Validate Base-view folders and kind filters |
| `duplicate_validation.py` | Find suspiciously similar filenames |
| `inbound_validation.py` | Find unlinked content notes, excluding self-contained views and daily journals |
| `section_validation.py` | Check expected sections for structured content notes |
| `tag_validation.py` | Validate frontmatter tag formats and prefixes |
| `master_validation.py` | Run every validation script and summarize results |
| `test_master.py` | Discover and run the unit tests in `agents/scripts/tests/` |

## Usage

```sh
python agents/scripts/frontmatter_validation.py
python agents/scripts/wikilink_validation.py
python agents/scripts/naming_validation.py
python agents/scripts/orphan_validation.py
```

Each validator exits `0` on success and `1` when issues are found. `template_validation.py` also runs safe in-memory regression cases for malformed frontmatter and an unmatched closing Markdown fence before checking vault files.

## Unit Tests

Run the unit-test runner to discover and execute tests in `agents/scripts/tests/`:

```sh
python agents/scripts/test_master.py
```

`test_master.py` runs unit tests only. Use `master_validation.py` for the full vault validation suite.

## Run All

```sh
for script in agents/scripts/*_validation.py; do
  python "$script" || echo "--- FAILED ---"
done
```
