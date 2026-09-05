import configparser
from pathlib import Path
from .tags import DEFAULT_INI, VALIDATOR_NAME, validate
def test_name(): assert VALIDATOR_NAME == "tags"

def test_hierarchical_tags_and_length_warning(tmp_path: Path):
    (tmp_path / "note.md").write_text("---\ntags: [python/project/developer, this_tag_name_is_far_too_long_for_the_policy]\n---\n",encoding="utf-8")
    config=configparser.ConfigParser(interpolation=None); config.read_string(DEFAULT_INI)
    issues,count=validate(tmp_path,config)
    assert count==1
    assert [(issue.code,issue.severity) for issue in issues]==[("TAG002","warning")]
