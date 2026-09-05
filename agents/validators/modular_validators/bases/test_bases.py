import configparser
from pathlib import Path
from .bases import DEFAULT_INI, VALIDATOR_NAME, validate
def test_name(): assert VALIDATOR_NAME == "bases"

def test_missing_folder_reference_is_an_error(tmp_path: Path):
    (tmp_path/"view.base").write_text('filters:\n  and:\n    - file.inFolder("missing")\n',encoding="utf-8")
    config=configparser.ConfigParser(interpolation=None); config.read_string(DEFAULT_INI)
    issues,count=validate(tmp_path,config)
    assert count==1
    assert [(issue.code,issue.severity) for issue in issues]==[("BASE001","error")]
