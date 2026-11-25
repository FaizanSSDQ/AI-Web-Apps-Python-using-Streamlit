"""Headless UI tests using Streamlit's AppTest (runs on the built-in sample dataset)."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_app_renders_sample_data():
    at = AppTest.from_file(str(APP)).run(timeout=60)
    assert not at.exception
    assert at.metric[0].value == "240"


def test_every_chart_type_renders_without_warning():
    at = AppTest.from_file(str(APP)).run(timeout=60)
    chart_select = next(s for s in at.selectbox if s.label == "Chart type")
    for kind in chart_select.options:
        chart_select.set_value(kind).run(timeout=60)
        assert not at.exception, kind
        assert not at.warning, f"{kind}: {[w.value for w in at.warning]}"
        chart_select = next(s for s in at.selectbox if s.label == "Chart type")
