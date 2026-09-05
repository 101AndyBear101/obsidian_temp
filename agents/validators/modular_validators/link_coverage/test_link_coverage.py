import configparser
from pathlib import Path
from .link_coverage import DEFAULT_INI, VALIDATOR_NAME, validate
def test_name(): assert VALIDATOR_NAME == "link_coverage"

def test_unlinked_note_gets_inbound_and_outbound_recommendations(tmp_path: Path):
    (tmp_path/"note.md").write_text("# Note\n",encoding="utf-8")
    config=configparser.ConfigParser(interpolation=None); config.read_string(DEFAULT_INI)
    issues,count=validate(tmp_path,config)
    assert count==1
    assert [(issue.code,issue.severity) for issue in issues]==[("COV001","warning"),("COV002","warning")]
