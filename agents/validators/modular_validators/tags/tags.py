#!/usr/bin/env python3
from __future__ import annotations

import argparse
import configparser
import difflib
import fnmatch
import json
import re
import sys
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, Iterable

try:
    import yaml
except ImportError:
    yaml = None



@dataclass(slots=True)
class Issue:
    severity: str
    code: str
    explanation: str
    path: str | None = None
    line: int | None = None
    column: int | None = None
    source_validator: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "explanation": self.explanation,
            "source_validator": self.source_validator,
            "location": None if self.path is None else {
                "path": self.path,
                "line": self.line,
                "column": self.column,
            },
        }


@dataclass(slots=True)
class RunResult:
    validator: str
    validation_path: str
    config_path: str | None
    started_at: str
    finished_at: str
    files_checked: int
    issues: list[Issue] = field(default_factory=list)
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    failure_code: int | None = None

    @property
    def exit_code(self) -> int:
        if self.failure_code is not None:
            return self.failure_code
        return 1 if any(issue.severity == "error" for issue in self.issues) else 0

    def to_dict(self) -> dict[str, Any]:
        warnings = sum(issue.severity == "warning" for issue in self.issues)
        errors = sum(issue.severity == "error" for issue in self.issues)
        return {
            "schema_version": 1,
            "run_id": self.run_id,
            "validator": self.validator,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "validation_path": self.validation_path,
            "config_path": self.config_path,
            "files_checked": self.files_checked,
            "issues": [issue.to_dict() for issue in self.issues],
            "summary": {"warnings": warnings, "errors": errors, "exit_code": self.exit_code},
        }


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parse_items(value: str) -> list[str]:
    return [item.strip() for item in value.replace(",", "\n").splitlines() if item.strip()]


def ignored(relative_path: str, patterns: Iterable[str]) -> bool:
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


def iter_files(validation_path: Path, suffixes: tuple[str, ...], patterns: Iterable[str] = ()) -> list[Path]:
    validation_path = validation_path.resolve()
    candidates = [validation_path] if validation_path.is_file() else validation_path.rglob("*")
    root = validation_path.parent if validation_path.is_file() else validation_path
    return [
        path for path in candidates
        if path.is_file()
        and path.suffix.lower() in suffixes
        and not ignored(path.relative_to(root).as_posix(), patterns)
    ]


def relative(path: Path, validation_path: Path) -> str:
    root = validation_path.parent if validation_path.is_file() else validation_path
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_frontmatter(path: Path) -> tuple[dict[str, Any] | None, int]:
    if yaml is None:
        raise RuntimeError("PyYAML is required; install dependencies from requirements.txt")
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("frontmatter has no closing delimiter") from exc
    try:
        parsed = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML frontmatter: {exc}") from exc
    if parsed is None:
        return {}, end + 1
    if not isinstance(parsed, dict):
        raise ValueError("frontmatter must be a mapping")
    return parsed, end + 1


def headings(text: str) -> set[str]:
    return set(re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE))


def config_path_for(script: Path) -> Path:
    return script.with_name(f"ini_{script.stem}.ini")


def log_path_for(script: Path) -> Path:
    return script.with_name(f"log_{script.stem}.json")


def load_config(script: Path, default_text: str) -> tuple[configparser.ConfigParser, Path, list[Issue]]:
    path = config_path_for(script)
    notices: list[Issue] = []
    if not path.exists():
        try:
            temporary = path.with_suffix(".ini.tmp")
            temporary.write_text(default_text.rstrip() + "\n", encoding="utf-8")
            temporary.replace(path)
            notices.append(Issue("warning", "CFG001", "Missing configuration was regenerated from defaults."))
        except OSError as exc:
            raise RuntimeError(f"could not regenerate {path}: {exc}") from exc
    parser = configparser.ConfigParser(interpolation=None)
    try:
        with path.open(encoding="utf-8") as stream:
            parser.read_file(stream)
    except (OSError, configparser.Error) as exc:
        raise RuntimeError(f"invalid configuration {path}: {exc}") from exc
    return parser, path, notices


def append_log(path: Path, result: RunResult) -> None:
    malformed: list[int] = []
    if path.exists():
        with path.open(encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    json.loads(line)
                except json.JSONDecodeError:
                    malformed.append(number)
    if malformed:
        lines = ", ".join(map(str, malformed))
        result.issues.append(Issue("warning", "LOG001", f"Existing log contains malformed JSON on line(s): {lines}."))
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result.to_dict(), ensure_ascii=False, separators=(",", ":")) + "\n")


Validator = Callable[[Path, configparser.ConfigParser], tuple[list[Issue], int]]


def run_validator(name: str, script: Path, default_ini: str, validation_path: Path, validate: Validator) -> RunResult:
    started = now()
    config, config_path, notices = load_config(script, default_ini)
    patterns = parse_items(config.get("ignore", "patterns", fallback=""))
    if not config.has_section("ignore"):
        config.add_section("ignore")
    config.set("ignore", "patterns", "\n".join(dict.fromkeys(patterns)))
    issues, count = validate(validation_path, config)
    return RunResult(name, str(validation_path.resolve()), str(config_path.resolve()), started, now(), count, notices + issues)


def record_result(script: Path, result: RunResult) -> None:
    if __import__("os").environ.get("VAULT_VALIDATION_MASTER_RUN") == "1":
        print(json.dumps(result.to_dict(), ensure_ascii=False, separators=(",", ":")))
        return
    append_log(log_path_for(script), result)


def execute_cli(name: str, script: Path, default_ini: str, validate: Validator) -> None:
    parser = argparse.ArgumentParser(description=f"Run the {name} vault validator.")
    parser.add_argument("--validation_path", type=Path, required=True)
    args = parser.parse_args()
    if not args.validation_path.exists():
        parser.error("--validation_path does not exist")
    try:
        result = run_validator(name, script, default_ini, args.validation_path, validate)
        record_result(script, result)
    except Exception as exc:
        print(f"{name}: {exc}", file=sys.stderr)
        timestamp = now()
        failed = RunResult(
            name,
            str(args.validation_path.resolve()),
            str(config_path_for(script).resolve()),
            timestamp,
            timestamp,
            0,
            [Issue("error", "RUN001", str(exc))],
            failure_code=2,
        )
        try:
            record_result(script, failed)
        except OSError:
            pass
        raise SystemExit(2) from exc
    print(f"{name}: {result.files_checked} files, {len(result.issues)} issues")
    raise SystemExit(result.exit_code)


VALIDATOR_NAME = "tags"
DEFAULT_INI = """[ignore]\npatterns =\n[rules]\nsegment_pattern = ^[a-z0-9]+(?:[-_][a-z0-9]+)*$\nwarning_length = 30\nignore_tags =\n"""
def validate(root: Path, config):
    files=iter_files(root,(".md",),parse_items(config.get("ignore","patterns",fallback="")))
    regex=re.compile(config.get("rules","segment_pattern")); limit=config.getint("rules","warning_length"); ignored=set(parse_items(config.get("rules","ignore_tags",fallback="")))
    issues=[]
    for path in files:
        rel=relative(path,root)
        try: fm,_=load_frontmatter(path)
        except Exception: continue
        if not fm or not fm.get("tags"): continue
        if not isinstance(fm["tags"],list): continue
        for tag in fm["tags"]:
            if tag in ignored: continue
            if not isinstance(tag,str) or any(not segment or not regex.fullmatch(segment) for segment in str(tag).split("/")):
                issues.append(Issue("error","TAG001",f"Invalid tag: {tag!r}.",rel,1))
            elif len(tag)>limit: issues.append(Issue("warning","TAG002",f"Tag {tag!r} exceeds {limit} characters.",rel,1))
    return issues,len(files)
if __name__ == "__main__": execute_cli(VALIDATOR_NAME,Path(__file__),DEFAULT_INI,validate)
