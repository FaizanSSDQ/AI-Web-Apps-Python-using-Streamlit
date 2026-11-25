"""Headless UI test using Streamlit's AppTest."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_analysis_runs_on_pasted_text():
    at = AppTest.from_file(str(APP)).run(timeout=60)
    assert not at.exception
    at.text_area[0].input("Firmware engineers write firmware for embedded firmware devices.").run()
    assert not at.exception
    assert at.metric[0].value == "8"
    at.text_input[0].input("firmware").run()
    assert at.metric[-2].value == "3"
