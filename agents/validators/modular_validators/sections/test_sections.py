import configparser
from pathlib import Path
from .sections import DEFAULT_INI, VALIDATOR_NAME, validate
def test_name(): assert VALIDATOR_NAME == "sections"

def test_permanent_note_without_expected_section_warns(tmp_path: Path):
    (tmp_path/"note.md").write_text("---\nkind: note\ntype: permanent\n---\n# Title\n",encoding="utf-8")
    config=configparser.ConfigParser(interpolation=None); config.read_string(DEFAULT_INI)
    issues,count=validate(tmp_path,config)
    assert count==1
    assert [(issue.code,issue.severity) for issue in issues]==[("SEC001","warning")]
