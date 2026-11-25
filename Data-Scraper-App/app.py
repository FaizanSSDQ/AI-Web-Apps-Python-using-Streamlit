"""
Web Data Scraper - Streamlit UI.

Run:  streamlit run app.py

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

import pandas as pd
import requests
import streamlit as st

from scraper import build_image_zip, http_fetch_bytes, scrape

st.set_page_config(page_title="Web Data Scraper", page_icon="🕸️", layout="wide")
st.title("🕸️ Web Data Scraper")
st.caption(
    "Extract text, headings, links, images and tables from any public web page, "
    "then export them as CSV or ZIP."
)

with st.form("scrape_form"):
    url = st.text_input("Web page URL", placeholder="https://en.wikipedia.org/wiki/Embedded_system")
    submitted = st.form_submit_button("Scrape", type="primary")

if submitted:
    try:
        with st.spinner("Fetching and parsing the page..."):
            st.session_state["page"] = scrape(url)
    except ValueError as exc:
        st.error(str(exc))
    except requests.RequestException as exc:
        st.error(f"Could not fetch the page: {exc}")

page = st.session_state.get("page")
if page is None:
    st.info("Enter a URL to begin. Please respect each website's terms of use and robots.txt.")
    st.stop()

st.subheader(page.title or "Untitled page")
st.caption(page.url)
if page.description:
    st.write(page.description)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Words", f"{page.word_count:,}")
c2.metric("Headings", len(page.headings))
c3.metric("Links", len(page.links))
c4.metric("Images", len(page.images))
c5.metric("Tables", len(page.tables))

tab_text, tab_links, tab_images, tab_tables = st.tabs(
    ["📝 Text", "🔗 Links", "🖼️ Images", "📊 Tables"]
)

with tab_text:
    if page.headings:
        st.markdown("**Heading outline**")
        st.dataframe(pd.DataFrame(page.headings), hide_index=True)
    st.text_area("Page text", page.text, height=300)
    st.download_button("⬇️ Download text (.txt)", page.text, file_name="page_text.txt")

with tab_links:
    if page.links:
        links = pd.DataFrame(page.links)
        kinds = st.multiselect(
            "Link types", sorted(links["type"].unique()), default=sorted(links["type"].unique())
        )
        filtered = links[links["type"].isin(kinds)]
        st.dataframe(
            filtered,
            hide_index=True,
            column_config={"url": st.column_config.LinkColumn("url")},
        )
        st.download_button(
            "⬇️ Download links (.csv)", filtered.to_csv(index=False), file_name="links.csv"
        )
    else:
        st.write("No links found.")

with tab_images:
    if page.images:
        images = pd.DataFrame(page.images)
        preview = images.head(24)
        cols = st.columns(4)
        for i, row in preview.iterrows():
            with cols[i % 4]:
                st.image(row["url"], caption=row["alt"][:60] or None, width="stretch")
        if len(images) > len(preview):
            st.caption(f"Showing {len(preview)} of {len(images)} images.")
        d1, d2 = st.columns(2)
        d1.download_button(
            "⬇️ Image list (.csv)", images.to_csv(index=False), file_name="images.csv"
        )
        if d2.button("📦 Prepare ZIP of images (max 50)"):
            with st.spinner("Downloading images..."):
                data, saved = build_image_zip(images["url"].tolist(), http_fetch_bytes)
            st.download_button(f"⬇️ Download ZIP ({saved} images)", data, file_name="images.zip")
    else:
        st.write("No images found.")

with tab_tables:
    if page.tables:
        for i, table in enumerate(page.tables, start=1):
            st.markdown(f"**Table {i}** · {table.shape[0]} rows × {table.shape[1]} columns")
            st.dataframe(table)
            st.download_button(
                f"⬇️ Table {i} (.csv)",
                table.to_csv(index=False),
                file_name=f"table_{i}.csv",
                key=f"table_{i}",
            )
    else:
        st.write("No HTML tables found on this page.")

st.divider()
st.caption("Built by [Faizan Saleem Siddiqui](https://github.com/FaizanSSDQ)")
