"""
Data Visualization App - Streamlit UI.

Run:  streamlit run app.py

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

import streamlit as st

from viz import (
    AGGREGATIONS,
    CHART_TYPES,
    SUPPORTED_FILES,
    build_chart,
    columns_by_type,
    load_table,
    profile,
    sample_dataset,
)

st.set_page_config(page_title="Data Visualization App", page_icon="📊", layout="wide")
st.title("📊 Data Visualization App")
st.caption("Upload CSV, Excel or JSON files, explore them and build interactive charts in seconds.")


@st.cache_data(show_spinner=False)
def read_file(data: bytes, name: str):
    return load_table(data, name)


# ---- Data source ---------------------------------------------------------------
with st.sidebar:
    st.header("Data")
    uploads = st.file_uploader(
        "Upload one or more files", type=list(SUPPORTED_FILES), accept_multiple_files=True
    )

datasets = {}
for file in uploads or []:
    try:
        datasets[file.name] = read_file(file.getvalue(), file.name)
    except Exception as exc:
        st.sidebar.error(f"{file.name}: could not be read ({exc})")
if not datasets:
    datasets["Sample: IoT sensor readings"] = sample_dataset()

with st.sidebar:
    name = st.selectbox("Active dataset", list(datasets))
df = datasets[name]
groups = columns_by_type(df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Columns", df.shape[1])
c3.metric("Numeric columns", len(groups["numeric"]))
c4.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")

tab_chart, tab_data, tab_profile = st.tabs(["📈 Chart builder", "🗂️ Data", "🔎 Column profile"])

# ---- Chart builder ---------------------------------------------------------------
with tab_chart:
    all_cols = list(df.columns)
    none = ["(none)"]
    left, right = st.columns([1, 3])
    with left:
        kind = st.selectbox("Chart type", CHART_TYPES)
        x = y = color = None
        agg = "sum"
        if kind in ("Line", "Bar", "Scatter", "Pie"):
            x_default = (
                groups["datetime"][0] if groups["datetime"] and kind == "Line" else all_cols[0]
            )
            x = st.selectbox("X axis / category", all_cols, index=all_cols.index(x_default))
            y = st.selectbox("Y value", groups["numeric"] or all_cols)
        elif kind == "Histogram":
            x = st.selectbox("Column", all_cols)
        elif kind == "Box":
            y = st.selectbox("Value", groups["numeric"] or all_cols)
            x_sel = st.selectbox("Group by", none + groups["categorical"])
            x = None if x_sel == "(none)" else x_sel
        if kind in ("Bar", "Pie"):
            agg = st.selectbox("Aggregation", AGGREGATIONS)
        if kind not in ("Pie", "Correlation heatmap"):
            c_sel = st.selectbox("Colour by", none + groups["categorical"])
            color = None if c_sel == "(none)" else c_sel
    with right:
        try:
            fig = build_chart(df, kind, x=x, y=y, color=color, agg=agg)
            st.plotly_chart(fig)
            st.download_button(
                "⬇️ Download chart (interactive HTML)",
                fig.to_html(include_plotlyjs="cdn"),
                file_name=f"{kind.lower().replace(' ', '_')}.html",
                mime="text/html",
            )
        except Exception as exc:
            st.warning(f"Cannot draw this chart with the current selection: {exc}")

# ---- Data -----------------------------------------------------------------------
with tab_data:
    query = st.text_input(
        "Filter rows with a pandas query (optional)",
        placeholder="temperature_c > 24 and node == 'Node-B'",
    )
    view = df
    if query:
        try:
            view = df.query(query)
        except Exception as exc:
            st.error(f"Invalid query: {exc}")
    st.dataframe(view)
    st.download_button("⬇️ Download as CSV", view.to_csv(index=False), file_name="data.csv")

# ---- Profile ----------------------------------------------------------------------
with tab_profile:
    st.dataframe(profile(df), hide_index=True)

st.divider()
st.caption("Built by [Faizan Saleem Siddiqui](https://github.com/FaizanSSDQ)")
