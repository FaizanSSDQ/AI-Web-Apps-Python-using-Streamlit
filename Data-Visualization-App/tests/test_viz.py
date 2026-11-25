"""Tests for data loading, profiling and chart building."""

import pandas as pd
import plotly.graph_objects as go
import pytest

from viz import CHART_TYPES, build_chart, columns_by_type, load_table, profile, sample_dataset


@pytest.fixture
def df():
    return sample_dataset()


def test_sample_dataset_is_deterministic(df):
    assert df.equals(sample_dataset())
    assert set(df["node"]) == {"Node-A", "Node-B", "Node-C"}


def test_columns_by_type(df):
    groups = columns_by_type(df)
    assert groups["datetime"] == ["date"]
    assert groups["categorical"] == ["node"]
    assert "temperature_c" in groups["numeric"]


@pytest.mark.parametrize("kind", CHART_TYPES)
def test_every_chart_type_builds(df, kind):
    args = {
        "Line": {"x": "date", "y": "temperature_c", "color": "node"},
        "Bar": {"x": "node", "y": "packets_lost", "agg": "mean"},
        "Scatter": {"x": "temperature_c", "y": "humidity_pct", "color": "node"},
        "Histogram": {"x": "battery_v"},
        "Box": {"x": "node", "y": "temperature_c"},
        "Pie": {"x": "node", "y": "packets_lost"},
        "Correlation heatmap": {},
    }[kind]
    assert isinstance(build_chart(df, kind, **args), go.Figure)


def test_missing_columns_raise(df):
    with pytest.raises(ValueError):
        build_chart(df, "Scatter", x="temperature_c", y=None)
    with pytest.raises(ValueError):
        build_chart(df[["node"]], "Correlation heatmap")


def test_load_csv_with_semicolons_and_dates():
    csv = b"date;value\n2025-01-01;1\n2025-01-02;2\n"
    loaded = load_table(csv, "readings.csv")
    assert list(loaded.columns) == ["date", "value"]
    assert pd.api.types.is_datetime64_any_dtype(loaded["date"])


def test_load_rejects_unknown_extension():
    with pytest.raises(ValueError):
        load_table(b"x", "file.parquet")


def test_profile_reports_missing_values():
    frame = pd.DataFrame({"a": [1.0, None, 3.0], "b": ["x", "y", "y"]})
    result = profile(frame).set_index("column")
    assert result.loc["a", "missing %"] == pytest.approx(33.3)
    assert result.loc["b", "unique"] == 2
