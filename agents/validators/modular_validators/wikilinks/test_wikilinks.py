import configparser
from pathlib import Path
from .wikilinks import DEFAULT_INI, VALIDATOR_NAME, validate
def test_name(): assert VALIDATOR_NAME == "wikilinks"

def test_missing_target_is_an_error(tmp_path: Path):
    (tmp_path/"source.md").write_text("[[missing-note]]",encoding="utf-8")
    config=configparser.ConfigParser(interpolation=None); config.read_string(DEFAULT_INI)
    issues,count=validate(tmp_path,config)
    assert count==1
    assert [(issue.code,issue.severity,issue.line) for issue in issues]==[("LINK001","error",1)]
