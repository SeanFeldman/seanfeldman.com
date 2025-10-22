from pathlib import Path
from orchard2md.parser import parse_export


def test_parse_minimal_xml(tmp_path: Path):
    fixture = Path("examples/fixtures/sample_orchard.xml")
    posts = parse_export(fixture, fmt="xml")
    assert len(posts) == 1
    p = posts[0]
    assert p["title"] == "Sample Post"
    assert p["slug"] == "sample-post"
    assert p["published"] is True
    assert "<strong>world</strong>" in (p["body_html"] or "")
