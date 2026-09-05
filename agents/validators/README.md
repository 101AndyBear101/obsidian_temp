---
kind: guide
status: active
created: 2026-09-03
tags:
  - vault/validation
---

# Vault Validation

The validation suite checks an Obsidian vault through independent, reusable Python validators. Python 3.10 or newer is required.

## Installation

Install runtime dependencies from this folder with `pip install -r agents/validators/requirements.txt`. Contributors should use `pip install -r agents/validators/requirements-dev.txt` to include pytest.

## Running Validation

Recursively discover and run every available validator:

```sh
python agents/validators/master.py --validation_path .
```

Run one validator directly:

```sh
python agents/validators/modular_validators/tags/tags.py --validation_path .
```

`--validation_path` is required and may identify one file or a directory. There are no output or configuration arguments.

## Layout

Each folder under `modular_validators/` uses its validator name for every file. For example, `bases/` contains `bases.py`, `test_bases.py`, `ini_bases.ini`, and the generated `log_bases.json`. A direct validator run appends one JSON Lines record to its local log. A master run collects each validator’s result without creating local logs, then appends the combined result beside `master.py` as `log_master.json`.

Every validator is standalone and contains its own configuration, discovery, parsing, result, and logging code. It does not import another validation script. The master recursively searches its directory and all subdirectories for non-test Python files that declare `VALIDATOR_NAME`. It runs every matching script it finds; absent validator scripts do not stop discovery or execution.

## Configuration

`ini_master.ini` controls recursive master discovery and the vault-wide directories to exclude. The master builds a filtered validation view from those patterns and passes only that directory to each validator. Each validator's neighboring `ini_<name>.ini` holds its specific rules and any unique local exceptions. Paths use forward slashes and are relative to the validation root.

If a local INI is missing, the validator regenerates its documented defaults, records warning `CFG001`, and continues. Invalid configuration stops the run with exit code `2` and is never overwritten automatically.

## Logs and Exit Codes

Logs use JSON Lines. Each line is one complete, versioned run object containing timestamps, paths, issue codes and explanations, locations, counts, and an exit code. Missing logs are created. Existing history is retained indefinitely. Malformed old lines are preserved and reported as `LOG001` in the next record.

See [[agents/validators/error-codes|Validation Issue Codes]] for the stable code catalog.

- `0`: no validation errors; warnings are allowed.
- `1`: one or more validation errors.
- `2`: configuration or execution failure.

## Tests

Recursively discover and run every unit-test file with:

```sh
python agents/validators/test_master.py
```

`test_master.py` continues through all discovered test files and reports a failing exit code after every test file has run.
