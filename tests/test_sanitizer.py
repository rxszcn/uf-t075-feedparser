import feedparser.sanitizer


def test_style_attr_is_enabled():
    html = """<p style="margin: 15em;">example</p>"""
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert result == html


def test_style_attr_can_be_disabled():
    html = """<p style="margin: 15em;">example</p>"""
    expected = """<p>example</p>"""
    original_attrs = feedparser.sanitizer.HTMLSanitizer.acceptable_attributes
    feedparser.sanitizer.HTMLSanitizer.acceptable_attributes = set()
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    feedparser.sanitizer.HTMLSanitizer.acceptable_attributes = original_attrs
    assert result == expected


def test_summary_element_is_preserved_with_nesting():
    # <summary> is an allowlisted element and must keep its tag and the
    # nested structure instead of being flattened to bare text.
    html = "<details><summary>click me</summary><p>body</p></details>"
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert result == html


def test_summary_element_keeps_nested_markup():
    html = (
        '<details open><summary><b>bold</b> title</summary>'
        "<p>text</p></details>"
    )
    expected = (
        '<details open="open"><summary><b>bold</b> title</summary>'
        "<p>text</p></details>"
    )
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert result == expected


def test_picture_element_round_trip():
    # <picture> wraps void <source> children and a fallback <img>;
    # the responsive structure must survive sanitization intact.
    html = (
        '<picture><source media="(min-width: 600px)" srcset="big.jpg">'
        '<img src="small.jpg" alt="x"></picture>'
    )
    expected = (
        '<picture><source media="(min-width: 600px)" srcset="big.jpg" />'
        '<img alt="x" src="small.jpg" /></picture>'
    )
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert result == expected


def test_picture_round_trip_with_full_responsive_attributes():
    html = (
        "<picture>"
        '<source type="image/webp" '
        'srcset="x.webp 1x, y.webp 2x" '
        'sizes="(min-width: 600px) 50vw, 100vw">'
        '<img src="x.jpg" alt="x">'
        "</picture>"
    )
    expected = (
        "<picture>"
        '<source sizes="(min-width: 600px) 50vw, 100vw" '
        'srcset="x.webp 1x, y.webp 2x" type="image/webp" />'
        '<img alt="x" src="x.jpg" />'
        "</picture>"
    )
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert result == expected


def test_img_srcset_and_sizes_are_preserved():
    html = (
        '<img src="fallback.jpg" srcset="a.jpg 1x, b.jpg 2x" '
        'alt="x" sizes="100vw">'
    )
    expected = (
        '<img alt="x" sizes="100vw" src="fallback.jpg" '
        'srcset="a.jpg 1x, b.jpg 2x" />'
    )
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert result == expected


def test_picture_strips_disallowed_attributes_but_keeps_structure():
    html = (
        '<picture><source srcset="big.jpg" onload="alert(1)">'
        '<img src="small.jpg" onclick="alert(2)"></picture>'
    )
    expected = (
        '<picture><source srcset="big.jpg" />'
        '<img src="small.jpg" /></picture>'
    )
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert result == expected


def test_source_outside_picture_round_trip_is_unchanged():
    # Guard against regressions of the pre-existing <source> output form
    # (void element rendered with the XHTML-style self-closing tag).
    html = '<audio controls><source src="a.ogg" type="audio/ogg"></audio>'
    expected = (
        '<audio controls="controls">'
        '<source src="a.ogg" type="audio/ogg" /></audio>'
    )
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert result == expected
