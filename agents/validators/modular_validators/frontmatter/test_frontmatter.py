import configparser
from pathlib import Path
from .frontmatter import DEFAULT_INI, VALIDATOR_NAME, validate

def test_name():
    assert VALIDATOR_NAME == "frontmatter"

def test_missing_note_type_is_a_recommendation(tmp_path: Path):
    (tmp_path / "note.md").write_text("---\nkind: note\nstatus: active\ncreated: 2026-09-03\ntags: [python]\n---\n", encoding="utf-8")
    config = configparser.ConfigParser(interpolation=None); config.read_string(DEFAULT_INI)
    issues, count = validate(tmp_path, config)
    assert count == 1
    assert [(issue.code, issue.severity) for issue in issues] == [("META006", "warning")]
