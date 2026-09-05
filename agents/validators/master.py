#!/usr/bin/env python3
from __future__ import annotations

import argparse
import configparser
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT = Path(__file__).resolve()
DEFAULT_CONFIG = """[discovery]
ignore_directories = __pycache__, .pytest_cache
[validation]
ignore_patterns = .git/**, .obsidian/**, .pytest_cache/**, **/__pycache__/**
"""


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parse_items(value: str) -> list[str]:
    return [item.strip() for item in value.replace(",", "\n").splitlines() if item.strip()]


def ignored(relative_path: str, patterns: list[str]) -> bool:
    normalized = relative_path.replace("\\", "/")
    for pattern in patterns:
        clean = pattern.replace("\\", "/").strip()
        if not clean:
            continue
        if clean.endswith("/**"):
            prefix = clean[:-3].rstrip("/")
            if normalized == prefix or normalized.startswith(prefix + "/"):
                return True
            if fnmatch.fnmatchcase(normalized + "/__directory__", clean):
                return True
        if fnmatch.fnmatchcase(normalized, clean):
            return True
    return False


def build_validation_view(source: Path, destination: Path, ignore_patterns: list[str]) -> Path:
    source = source.resolve()
    if source.is_file():
        if ignored(source.name, ignore_patterns):
            raise RuntimeError("The requested file is excluded by the master ignore patterns.")
        destination.mkdir(parents=True, exist_ok=True)
        copied = destination / source.name
        shutil.copy2(source, copied)
        return copied

    destination.mkdir(parents=True, exist_ok=True)
    for path in source.rglob("*"):
        relative_path = path.relative_to(source).as_posix()
        if ignored(relative_path, ignore_patterns):
            continue
        target = destination / relative_path
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    return destination


def load_master_config() -> tuple[configparser.ConfigParser, Path, bool]:
    path = SCRIPT.with_name("ini_master.ini")
    regenerated = not path.exists()
    if regenerated:
        temporary = path.with_suffix(".ini.tmp")
        temporary.write_text(DEFAULT_CONFIG, encoding="utf-8")
        temporary.replace(path)
    config = configparser.ConfigParser(interpolation=None)
    try:
        with path.open(encoding="utf-8") as stream:
            config.read_file(stream)
    except (OSError, configparser.Error) as exc:
        raise RuntimeError(f"invalid master configuration: {exc}") from exc
    return config, path, regenerated


def discover_validation_scripts(
    search_root: Path | None = None,
    ignored_directories: set[str] | None = None,
) -> list[Path]:
    root = (search_root or SCRIPT.parent).resolve()
    ignored = ignored_directories or {"__pycache__", ".pytest_cache"}
    discovered: list[Path] = []
    for path in root.rglob("*.py"):
        relative_parts = path.relative_to(root).parts
        if any(part in ignored for part in relative_parts):
            continue
        if path.resolve() == SCRIPT or path.name.startswith("test_"):
            continue
        if path.name == "remove_internal_prompts.py":
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if not re.search(r"^VALIDATOR_NAME\s*=", source, re.MULTILINE):
            continue
        discovered.append(path.resolve())
    return sorted(discovered, key=lambda path: path.as_posix().lower())


def _child_record(output: str) -> dict[str, Any] | None:
    for line in reversed(output.splitlines()):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            return record
    return None


def run_validation_script(script: Path, validation_path: Path) -> dict[str, Any]:
    environment = os.environ.copy()
    environment["VAULT_VALIDATION_MASTER_RUN"] = "1"
    completed = subprocess.run(
        [sys.executable, str(script), "--validation_path", str(validation_path)],
        cwd=SCRIPT.parent.parent.parent,
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )
    record = _child_record(completed.stdout)
    if record is None:
        return {
            "validator": script.stem,
            "script": script.relative_to(SCRIPT.parent).as_posix(),
            "files_checked": 0,
            "issues": [{
                "severity": "error",
                "code": "RUN001",
                "explanation": completed.stderr.strip() or "Validator did not append a readable log record.",
                "source_validator": script.stem,
                "location": {"path": script.relative_to(SCRIPT.parent).as_posix(), "line": None, "column": None},
            }],
            "summary": {"warnings": 0, "errors": 1, "exit_code": 2},
        }
    record["script"] = script.relative_to(SCRIPT.parent).as_posix()
    if completed.returncode not in (0, 1, 2):
        record["issues"].append({
            "severity": "error",
            "code": "RUN001",
            "explanation": f"Validator exited with unexpected code {completed.returncode}.",
            "source_validator": script.stem,
            "location": {"path": record["script"], "line": None, "column": None},
        })
        record["summary"]["errors"] += 1
        record["summary"]["exit_code"] = 2
    return record


def append_master_log(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def build_master_record(
    validation_path: Path,
    config_path: Path,
    started_at: str,
    children: list[dict[str, Any]],
    regenerated: bool,
) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    if regenerated:
        issues.append({
            "severity": "warning",
            "code": "CFG001",
            "explanation": "Missing master configuration was regenerated from defaults.",
            "source_validator": None,
            "location": None,
        })
    if not children:
        issues.append({
            "severity": "warning",
            "code": "RUN002",
            "explanation": "No validation scripts were discovered.",
            "source_validator": None,
            "location": None,
        })
    for child in children:
        for original in child.get("issues", []):
            issue = dict(original)
            issue["source_validator"] = child.get("validator")
            issues.append(issue)
    warnings = sum(issue.get("severity") == "warning" for issue in issues)
    errors = sum(issue.get("severity") == "error" for issue in issues)
    child_codes = [child.get("summary", {}).get("exit_code", 2) for child in children]
    exit_code = 2 if 2 in child_codes else 1 if errors else 0
    return {
        "schema_version": 1,
        "run_id": uuid.uuid4().hex,
        "validator": "master",
        "started_at": started_at,
        "finished_at": now(),
        "validation_path": str(validation_path.resolve()),
        "config_path": str(config_path.resolve()),
        "files_checked": sum(int(child.get("files_checked", 0)) for child in children),
        "issues": issues,
        "validators": [{
            "validator": child.get("validator"),
            "script": child.get("script"),
            "summary": child.get("summary"),
        } for child in children],
        "summary": {"warnings": warnings, "errors": errors, "exit_code": exit_code},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover and run every vault validator.")
    parser.add_argument("--validation_path", type=Path, required=True)
    args = parser.parse_args()
    if not args.validation_path.exists():
        parser.error("--validation_path does not exist")
    started_at = now()
    try:
        config, config_path, regenerated = load_master_config()
        ignored = set(parse_items(config.get("discovery", "ignore_directories", fallback="")))
        scripts = discover_validation_scripts(ignored_directories=ignored)
        validation_ignores = parse_items(config.get("validation", "ignore_patterns", fallback=""))
        children: list[dict[str, Any]] = []
        with tempfile.TemporaryDirectory(prefix="vault-validation-") as temporary_directory:
            validation_view = build_validation_view(
                args.validation_path, Path(temporary_directory), validation_ignores
            )
            for script in scripts:
                child = run_validation_script(script, validation_view)
                children.append(child)
                summary = child["summary"]
                state = "PASS" if summary["exit_code"] == 0 else "FAIL"
                print(f"[{state}] {child['validator']}: {child['files_checked']} files, "
                      f"{summary['errors']} errors, {summary['warnings']} warnings")
        result = build_master_record(
            args.validation_path, config_path, started_at, children, regenerated
        )
        append_master_log(SCRIPT.with_name("log_master.json"), result)
    except Exception as exc:
        print(f"master: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    raise SystemExit(result["summary"]["exit_code"])


if __name__ == "__main__":
    main()
