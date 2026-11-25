"""Headless UI tests using Streamlit's AppTest (no network calls are made)."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_app_starts_without_errors():
    at = AppTest.from_file(str(APP)).run(timeout=60)
    assert not at.exception
    assert at.title[0].value.endswith("YouTube Keyword Extractor")


def test_invalid_link_shows_error():
    at = AppTest.from_file(str(APP)).run(timeout=60)
    at.text_input[0].input("https://vimeo.com/12345")
    at.button[0].click().run(timeout=60)
    assert not at.exception
    assert "video ID" in at.error[0].value
