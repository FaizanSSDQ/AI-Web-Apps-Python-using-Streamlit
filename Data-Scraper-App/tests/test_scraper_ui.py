"""Headless UI smoke test using Streamlit's AppTest."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_app_starts_without_errors():
    at = AppTest.from_file(str(APP)).run(timeout=60)
    assert not at.exception
    assert at.title[0].value.endswith("Web Data Scraper")
