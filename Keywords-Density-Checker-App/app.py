"""
Keyword Density Checker - Streamlit UI.

Run:  streamlit run app.py

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

import requests
import streamlit as st

from density import keyword_density, target_keyword_report, text_from_url, text_stats

st.set_page_config(page_title="Keyword Density Checker", page_icon="🔑", layout="wide")
st.title("🔑 Keyword Density Checker")
st.caption(
    "Analyse keyword and phrase frequency in any text, file or web page for SEO and writing."
)

with st.sidebar:
    st.header("Analysis options")
    phrase_len = st.radio(
        "Phrase length", [1, 2, 3], format_func=lambda n: f"{n}-word", horizontal=True
    )
    remove_stop = st.checkbox("Ignore common stopwords", value=True)
    min_len = st.slider("Minimum word length", 1, 6, 3)
    top_k = st.slider("Show top N keywords", 5, 100, 25)

source = st.radio(
    "Text source", ["Paste text", "Upload .txt file", "Web page URL"], horizontal=True
)
text = ""
if source == "Paste text":
    text = st.text_area(
        "Your text", height=220, placeholder="Paste an article, blog post or product description..."
    )
elif source == "Upload .txt file":
    file = st.file_uploader("Text file", type=["txt", "md"])
    if file:
        text = file.getvalue().decode("utf-8", errors="ignore")
else:
    url = st.text_input("Page URL", placeholder="https://example.com/article")
    if url and st.button("Fetch page"):
        try:
            st.session_state["url_text"] = text_from_url(url)
        except requests.RequestException as exc:
            st.error(f"Could not fetch the page: {exc}")
    text = st.session_state.get("url_text", "")
    if text:
        with st.expander("Extracted text"):
            st.write(text[:5000] + ("..." if len(text) > 5000 else ""))

if not text.strip():
    st.info("Provide some text to analyse.")
    st.stop()

stats = text_stats(text)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Words", f"{stats['words']:,}")
c2.metric("Unique words", f"{stats['unique_words']:,}")
c3.metric("Sentences", stats["sentences"])
c4.metric("Words / sentence", stats["avg_words_per_sentence"])
c5.metric("Reading time", f"{stats['reading_time_min']} min")

table = keyword_density(
    text, n=phrase_len, remove_stopwords=remove_stop, min_length=min_len, top_k=top_k
)

left, right = st.columns([2, 3])
with left:
    st.subheader("Top keywords")
    st.dataframe(
        table,
        hide_index=True,
        column_config={"density_%": st.column_config.NumberColumn("density %", format="%.2f")},
    )
    st.download_button("⬇️ Download CSV", table.to_csv(index=False), file_name="keyword_density.csv")
with right:
    st.subheader("Frequency chart")
    if not table.empty:
        st.bar_chart(table.head(20), x="keyword", y="count", horizontal=True, sort="-count")
    else:
        st.write("No keywords match the current filters.")

st.subheader("🎯 Target keyword check")
keyword = st.text_input("Keyword or phrase to check", placeholder="embedded systems")
if keyword:
    report = target_keyword_report(text, keyword)
    k1, k2 = st.columns(2)
    k1.metric("Occurrences", report["count"])
    k2.metric("Density", f"{report['density']} %")
    st.write(report["verdict"])

st.divider()
st.caption("Built by [Faizan Saleem Siddiqui](https://github.com/FaizanSSDQ)")
