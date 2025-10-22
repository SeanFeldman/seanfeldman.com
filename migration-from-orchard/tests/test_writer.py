from pathlib import Path
from orchard2md.writer import render_front_matter, write_post_file


def test_front_matter_yaml():
    post = {
        "title": "Sample Post",
        "slug": "sample-post",
        "created": "2020-01-02T03:04:05Z",
        "published": True,
        "tags": ["orchard", "export"],
    }
    fm = render_front_matter(post)
    assert fm.startswith("---\n") and fm.endswith("\n---\n") is False  # ending handled in writer
    assert "title: Sample Post" in fm
    assert "slug: sample-post" in fm


def test_write_file(tmp_path: Path):
    post = {
        "title": "Sample Post",
        "slug": "sample-post",
        "created": "2020-01-02T03:04:05Z",
        "published": True,
    }
    p = write_post_file(tmp_path, "2020-01-02-sample-post.md", post, "Body\n")
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "Body" in text
