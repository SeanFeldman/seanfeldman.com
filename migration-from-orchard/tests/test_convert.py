from orchard2md.convert import convert_html_to_markdown


def test_html_to_markdown_basic():
    html = "<p>Hello <strong>world</strong>!</p>"
    md = convert_html_to_markdown(html)
    assert "**world**" in md
