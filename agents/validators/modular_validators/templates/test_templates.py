import configparser
from pathlib import Path
from .templates import DEFAULT_INI, VALIDATOR_NAME, validate
def test_name(): assert VALIDATOR_NAME == "templates"

def test_unclosed_fence_is_an_error(tmp_path: Path):
    folder=tmp_path/"templates"; folder.mkdir()
    (folder/"broken.md").write_text("```mermaid\ngraph TD\n",encoding="utf-8")
    config=configparser.ConfigParser(interpolation=None); config.read_string(DEFAULT_INI)
    issues,count=validate(tmp_path,config)
    assert count==1
    assert [(issue.code,issue.severity) for issue in issues]==[("TPL001","error")]
