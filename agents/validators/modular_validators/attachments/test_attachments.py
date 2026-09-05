import configparser
from pathlib import Path
from .attachments import DEFAULT_INI, VALIDATOR_NAME, validate
def test_name(): assert VALIDATOR_NAME == "attachments"

def test_missing_embed_is_an_error(tmp_path: Path):
    (tmp_path/"note.md").write_text("![[missing-image.png]]",encoding="utf-8")
    config=configparser.ConfigParser(interpolation=None); config.read_string(DEFAULT_INI)
    issues,count=validate(tmp_path,config)
    assert count==1
    assert [(issue.code,issue.severity) for issue in issues]==[("ATT001","error")]
