import configparser
from pathlib import Path
from .duplicates import DEFAULT_INI, VALIDATOR_NAME, validate
def test_name(): assert VALIDATOR_NAME == "duplicates"

def test_similar_filenames_warn(tmp_path: Path):
    (tmp_path/"backup-check.md").touch(); (tmp_path/"backup-checks.md").touch()
    config=configparser.ConfigParser(interpolation=None); config.read_string(DEFAULT_INI)
    issues,count=validate(tmp_path,config)
    assert count==2
    assert [(issue.code,issue.severity) for issue in issues]==[("DUP001","warning")]
