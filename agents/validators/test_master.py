#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import master

SCRIPT = Path(__file__).resolve()


def discover_unit_tests(search_root: Path | None = None) -> list[Path]:
    root = (search_root or SCRIPT.parent.parent).resolve()
    discovered = []
    for path in root.rglob("test_*.py"):
        if "__pycache__" in path.parts or ".pytest_cache" in path.parts:
            continue
        discovered.append(path.resolve())
    return sorted(discovered, key=lambda path: path.as_posix().lower())


def run_all_unit_tests(
    search_root: Path | None = None,
    working_directory: Path | None = None,
) -> int:
    tests = discover_unit_tests(search_root)
    cwd = (working_directory or SCRIPT.parent.parent.parent).resolve()
    failed = False
    for test_file in tests:
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", str(test_file)],
            cwd=cwd,
            check=False,
        )
        state = "PASS" if completed.returncode == 0 else "FAIL"
        print(f"[{state}] {test_file}")
        failed = failed or completed.returncode != 0
    if not tests:
        print("No unit tests were discovered.")
    return 1 if failed else 0


def test_discovers_unit_tests_recursively(tmp_path: Path):
    first = tmp_path / "one" / "test_one.py"
    second = tmp_path / "nested" / "two" / "test_two.py"
    first.parent.mkdir(parents=True)
    second.parent.mkdir(parents=True)
    first.touch()
    second.touch()
    (tmp_path / "missing-test-folder").mkdir()

    expected = sorted([first.resolve(), second.resolve()], key=lambda path: path.as_posix().lower())
    assert discover_unit_tests(tmp_path) == expected


def test_runner_invokes_every_discovered_test(tmp_path: Path, monkeypatch):
    first = tmp_path / "one" / "test_one.py"
    second = tmp_path / "two" / "test_two.py"
    first.parent.mkdir()
    second.parent.mkdir()
    first.touch()
    second.touch()
    invoked: list[Path] = []

    def fake_run(command, **kwargs):
        invoked.append(Path(command[-1]))
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert run_all_unit_tests(tmp_path, tmp_path) == 0
    assert invoked == [first.resolve(), second.resolve()]


def test_real_tree_contains_every_validator_test():
    tests = set(discover_unit_tests())
    validator_root = SCRIPT.parent / "modular_validators"
    expected = set(validator_root.rglob("test_*.py"))
    assert expected <= tests


def test_master_discovers_validation_scripts_recursively_without_a_registry(tmp_path: Path):
    first = tmp_path / "one" / "anything.py"
    second = tmp_path / "nested" / "two" / "second.py"
    first.parent.mkdir(parents=True)
    second.parent.mkdir(parents=True)
    first.write_text('VALIDATOR_NAME = "one"\n', encoding="utf-8")
    second.write_text('VALIDATOR_NAME="two"\n', encoding="utf-8")
    (tmp_path / "missing-validator").mkdir()
    (tmp_path / "unrelated.py").write_text("print('utility')\n", encoding="utf-8")

    assert master.discover_validation_scripts(tmp_path) == sorted(
        [first.resolve(), second.resolve()], key=lambda path: path.as_posix().lower()
    )


def test_master_builds_a_filtered_validation_view(tmp_path: Path):
    source = tmp_path / "vault"
    destination = tmp_path / "filtered-vault"
    (source / "notes").mkdir(parents=True)
    (source / ".obsidian").mkdir()
    (source / "agents" / "scripts" / "__pycache__").mkdir(parents=True)
    (source / "notes" / "keep.md").write_text("# Keep\n", encoding="utf-8")
    (source / ".obsidian" / "state.json").write_text("{}", encoding="utf-8")
    (source / "agents" / "scripts" / "__pycache__" / "cached.pyc").write_bytes(b"cache")

    view = master.build_validation_view(source, destination, [".obsidian/**", "**/__pycache__/**"])

    assert view == destination
    assert (view / "notes" / "keep.md").is_file()
    assert not (view / ".obsidian").exists()
    assert not (view / "agents" / "scripts" / "__pycache__").exists()


def test_every_validator_script_is_standalone():
    scripts = master.discover_validation_scripts()
    assert scripts
    for script in scripts:
        source = script.read_text(encoding="utf-8")
        forbidden_shared_package = "validation" + "_common"
        assert forbidden_shared_package not in source
        assert "BUILTIN_IGNORES" not in source
        assert "from validators" not in source


if __name__ == "__main__":
    raise SystemExit(run_all_unit_tests())
