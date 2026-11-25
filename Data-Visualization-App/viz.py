"""
Data Visualization App - data loading, profiling and chart building.

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

from __future__ import annotations

import io

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

SUPPORTED_FILES = ("csv", "xlsx", "xls", "json")
CHART_TYPES = ("Line", "Bar", "Scatter", "Histogram", "Box", "Pie", "Correlation heatmap")
AGGREGATIONS = ("sum", "mean", "median", "count", "min", "max")


def load_table(data: bytes, filename: str) -> pd.DataFrame:
    """Read an uploaded CSV / Excel / JSON file into a DataFrame."""
    ext = filename.rsplit(".", 1)[-1].lower()
    buffer = io.BytesIO(data)
    if ext == "csv":
        df = pd.read_csv(buffer, sep=None, engine="python")  # auto-detect , ; \t
    elif ext in ("xlsx", "xls"):
        df = pd.read_excel(buffer)
    elif ext == "json":
        df = pd.read_json(buffer)
    else:
        raise ValueError(f"Unsupported file type: .{ext}")
    return parse_dates(df)


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convert text columns that look like dates (e.g. 'date', 'time') to datetime."""
    df = df.copy()
    for col in df.columns:
        if classify(df[col]) == "categorical" and any(
            k in str(col).lower() for k in ("date", "time")
        ):
            converted = pd.to_datetime(df[col], errors="coerce")
            if converted.notna().mean() > 0.8:
                df[col] = converted
    return df


def classify(series: pd.Series) -> str:
    """Return 'numeric', 'datetime' or 'categorical'."""
    if pd.api.types.is_bool_dtype(series):
        return "categorical"
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    return "categorical"


def columns_by_type(df: pd.DataFrame) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {"numeric": [], "datetime": [], "categorical": []}
    for col in df.columns:
        groups[classify(df[col])].append(col)
    return groups


def profile(df: pd.DataFrame) -> pd.DataFrame:
    """One row per column: type, completeness, cardinality and basic statistics."""
    rows = []
    for col in df.columns:
        s = df[col]
        kind = classify(s)
        row = {
            "column": col,
            "type": kind,
            "non-null": int(s.notna().sum()),
            "missing %": round(100 * s.isna().mean(), 1),
            "unique": int(s.nunique()),
            "mean": None,
            "min": None,
            "max": None,
        }
        if kind == "numeric":
            row.update(mean=round(float(s.mean()), 3), min=s.min(), max=s.max())
        elif kind == "datetime":
            row.update(min=str(s.min()), max=str(s.max()))
        rows.append(row)
    return pd.DataFrame(rows)


def build_chart(
    df: pd.DataFrame,
    kind: str,
    x: str | None = None,
    y: str | None = None,
    color: str | None = None,
    agg: str = "sum",
) -> go.Figure:
    """Build a Plotly figure. Raises ValueError when required columns are missing."""
    groups = columns_by_type(df)

    def need(*cols: str | None) -> None:
        if any(c is None or c not in df.columns for c in cols):
            raise ValueError(f"The '{kind}' chart needs a valid column for every axis.")

    if kind == "Line":
        need(x, y)
        data = df.sort_values(x)
        fig = px.line(data, x=x, y=y, color=color, markers=len(data) <= 60)
    elif kind == "Bar":
        need(x, y)
        keys = [x] + ([color] if color else [])
        data = df.groupby(keys, dropna=False)[y].agg(agg).reset_index()
        fig = px.bar(data, x=x, y=y, color=color, barmode="group")
        fig.update_layout(yaxis_title=f"{agg}({y})")
    elif kind == "Scatter":
        need(x, y)
        fig = px.scatter(df, x=x, y=y, color=color, opacity=0.75)
    elif kind == "Histogram":
        need(x)
        fig = px.histogram(df, x=x, color=color, barmode="overlay", opacity=0.75)
    elif kind == "Box":
        need(y)
        fig = px.box(df, x=x, y=y, color=color, points="outliers")
    elif kind == "Pie":
        need(x, y)
        data = df.groupby(x, dropna=False)[y].agg(agg).reset_index()
        fig = px.pie(data, names=x, values=y, hole=0.35)
    elif kind == "Correlation heatmap":
        numeric = groups["numeric"]
        if len(numeric) < 2:
            raise ValueError("A correlation heatmap needs at least two numeric columns.")
        corr = df[numeric].corr()
        fig = px.imshow(
            corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1, aspect="auto"
        )
    else:
        raise ValueError(f"Unknown chart type: {kind}")

    fig.update_layout(margin={"l": 10, "r": 10, "t": 40, "b": 10}, title=kind)
    return fig


def sample_dataset(rows: int = 240, seed: int = 7) -> pd.DataFrame:
    """Deterministic demo data: daily readings from three IoT sensor nodes."""
    rng = np.random.default_rng(seed)
    days = pd.date_range("2025-01-01", periods=rows // 3, freq="D")
    frames = []
    for node, (base_t, base_h) in {
        "Node-A": (22, 45),
        "Node-B": (26, 38),
        "Node-C": (19, 60),
    }.items():
        n = len(days)
        season = 4 * np.sin(np.linspace(0, 2 * np.pi, n))
        frames.append(
            pd.DataFrame(
                {
                    "date": days,
                    "node": node,
                    "temperature_c": np.round(base_t + season + rng.normal(0, 1.2, n), 2),
                    "humidity_pct": np.round(base_h - season * 1.5 + rng.normal(0, 3, n), 1),
                    "battery_v": np.round(np.linspace(4.15, 3.55, n) + rng.normal(0, 0.02, n), 3),
                    "packets_lost": rng.poisson(2, n),
                }
            )
        )
    return pd.concat(frames, ignore_index=True)
