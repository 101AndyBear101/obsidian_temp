import configparser
from pathlib import Path
from .indexes import DEFAULT_INI, VALIDATOR_NAME, validate
def test_name(): assert VALIDATOR_NAME == "indexes"

def test_index_without_links_warns(tmp_path: Path):
    (tmp_path/"INDEX.md").write_text("# Index\n",encoding="utf-8")
    config=configparser.ConfigParser(interpolation=None); config.read_string(DEFAULT_INI)
    issues,count=validate(tmp_path,config)
    assert count==1
    assert [(issue.code,issue.severity) for issue in issues]==[("IDX001","warning")]
