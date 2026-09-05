import configparser
from pathlib import Path
from .naming import DEFAULT_INI, VALIDATOR_NAME, validate
def test_name(): assert VALIDATOR_NAME == "naming"

def test_daily_names_require_real_iso_dates(tmp_path: Path):
    folder=tmp_path/"journals"/"daily"; folder.mkdir(parents=True)
    (folder/"2026-02-30.md").touch(); (folder/"2026-09-03.md").touch()
    config=configparser.ConfigParser(interpolation=None); config.read_string(DEFAULT_INI)
    issues,_=validate(tmp_path,config)
    assert [(issue.code,issue.path) for issue in issues]==[("NAME002","journals/daily/2026-02-30.md")]
