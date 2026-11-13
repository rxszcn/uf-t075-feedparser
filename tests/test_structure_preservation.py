import io

import feedparser
import feedparser.api

HTML_BODY = (
    "<details><summary>S</summary><p>P</p></details>\n"
    '<picture><source media="(min-width: 600px)" srcset="big.jpg">'
    '<img src="small.jpg" alt="a"></picture>'
)

ATOM_FEED = (
    b'<?xml version="1.0" encoding="utf-8"?>'
    b'<feed xmlns="http://www.w3.org/2005/Atom">'
    b"<title>example feed</title>"
    b"<entry><title>example entry</title>"
    b'<content type="html">'
    + HTML_BODY.encode("ascii").replace(b"<", b"&lt;").replace(b">", b"&gt;")
    + b"</content></entry></feed>"
)

EXPECTED = (
    "<details><summary>S</summary><p>P</p></details>\n"
    '<picture><source media="(min-width: 600px)" srcset="big.jpg" />'
    '<img alt="a" src="small.jpg" /></picture>'
)


def test_responsive_and_disclosure_structure_survives_strict_parser():
    d = feedparser.parse(io.BytesIO(ATOM_FEED))
    assert d.entries[0].content[0].value == EXPECTED


def test_responsive_and_disclosure_structure_survives_loose_parser(
    monkeypatch,
):
    monkeypatch.setattr(feedparser.api, "_XML_AVAILABLE", False)
    d = feedparser.parse(io.BytesIO(ATOM_FEED))
    assert d.entries[0].content[0].value == EXPECTED
