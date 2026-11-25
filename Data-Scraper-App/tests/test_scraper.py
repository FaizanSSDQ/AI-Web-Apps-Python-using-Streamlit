"""Tests for the scraping engine (offline: uses static HTML)."""

import io
import zipfile

import pytest

from scraper import build_image_zip, normalize_url, parse_page

HTML = """
<html><head><title> Sensor Catalog </title>
<meta name="description" content="Low-power sensors."></head>
<body>
  <h1>Sensors</h1><h2>IMUs</h2>
  <a href="/imu">IMU page</a>
  <a href="/imu">duplicate</a>
  <a href="https://other.org/x">External</a>
  <a href="mailto:hi@example.com">Mail</a>
  <a href="#top">skip</a>
  <img src="/img/bmi270.png" alt="BMI270">
  <img data-src="lazy.jpg">
  <img src="data:image/png;base64,AAAA">
  <table><tr><th>Part</th><th>Current (uA)</th></tr>
         <tr><td>BMI270</td><td>685</td></tr></table>
  <script>var x = 1;</script>
</body></html>
"""


@pytest.fixture
def page():
    return parse_page(HTML, "https://example.com/catalog/")


def test_metadata(page):
    assert page.title == "Sensor Catalog"
    assert page.description == "Low-power sensors."
    assert [h["level"] for h in page.headings] == ["H1", "H2"]


def test_links_are_absolute_deduplicated_and_typed(page):
    types = {link["url"]: link["type"] for link in page.links}
    assert types == {
        "https://example.com/imu": "internal",
        "https://other.org/x": "external",
        "mailto:hi@example.com": "email",
    }


def test_images_skip_data_uris_and_support_lazy_loading(page):
    assert [img["url"] for img in page.images] == [
        "https://example.com/img/bmi270.png",
        "https://example.com/catalog/lazy.jpg",
    ]


def test_tables_and_text(page):
    assert len(page.tables) == 1
    assert page.tables[0].iloc[0]["Part"] == "BMI270"
    assert "var x" not in page.text
    assert page.word_count > 0


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("example.com", "https://example.com"), (" http://a.io/x ", "http://a.io/x")],
)
def test_normalize_url(raw, expected):
    assert normalize_url(raw) == expected


@pytest.mark.parametrize("bad", ["", "not a url", "https://"])
def test_normalize_url_rejects_invalid(bad):
    with pytest.raises(ValueError):
        normalize_url(bad)


def test_build_image_zip_skips_failures():
    def fake_fetch(url):
        if "bad" in url:
            raise OSError("blocked")
        return b"img-bytes"

    data, saved = build_image_zip(["https://a.com/x.png", "https://a.com/bad.png"], fake_fetch)
    assert saved == 1
    names = zipfile.ZipFile(io.BytesIO(data)).namelist()
    assert names == ["001_x.png"]
