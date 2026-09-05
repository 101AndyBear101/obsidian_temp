import configparser
from pathlib import Path
from .skills import DEFAULT_INI, VALIDATOR_NAME, validate
def test_name(): assert VALIDATOR_NAME == "skills"

def test_skill_layout_and_registration_are_checked(tmp_path: Path):
    folder=tmp_path/"agents"/"skills"/"sample-skill"; folder.mkdir(parents=True)
    (folder.parent/"INDEX.md").write_text("# Skills\n",encoding="utf-8")
    config=configparser.ConfigParser(interpolation=None); config.read_string(DEFAULT_INI)
    issues,count=validate(tmp_path,config)
    assert count==1
    assert [(issue.code,issue.severity) for issue in issues]==[("SKILL002","error"),("SKILL003","warning")]
