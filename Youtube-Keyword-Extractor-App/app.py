"""
YouTube Keyword Extractor - Streamlit UI.

Run:  streamlit run app.py

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

import pandas as pd
import requests
import streamlit as st

from youtube import TAG_CHARACTER_LIMIT, fetch_video_info, format_duration

st.set_page_config(page_title="YouTube Keyword Extractor", page_icon="▶️", layout="wide")
st.title("▶️ YouTube Keyword Extractor")
st.caption(
    "See the hidden tags of any public YouTube video, plus its title, channel, views and hashtags."
)

with st.form("video_form"):
    link = st.text_input(
        "Video link or ID",
        placeholder="https://www.youtube.com/watch?v=...  ·  https://youtu.be/...  ·  /shorts/...",
    )
    submitted = st.form_submit_button("Extract keywords", type="primary")

if submitted:
    try:
        with st.spinner("Reading video page..."):
            st.session_state["video"] = fetch_video_info(link)
    except ValueError as exc:
        st.error(str(exc))
    except requests.RequestException as exc:
        st.error(f"Could not reach YouTube: {exc}")

video = st.session_state.get("video")
if video is None:
    st.info("Paste a YouTube link. Works with watch, youtu.be, Shorts, embed and live links.")
    st.stop()

left, right = st.columns([1, 2])
with left:
    st.image(video.thumbnail_url, width="stretch")
    st.link_button("Open on YouTube ↗", video.url)
with right:
    st.subheader(video.title or video.video_id)
    if video.channel:
        st.write(f"**Channel:** {video.channel}")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Views", f"{video.views:,}" if video.views is not None else "-")
    m2.metric("Duration", format_duration(video.length_seconds))
    m3.metric("Tags", len(video.keywords))
    m4.metric("Category", video.category or "-")
    if video.publish_date:
        st.caption(f"Published {video.publish_date}")

st.subheader("🏷️ Tags")
if video.keywords:
    used = video.tags_character_count
    st.progress(
        min(used / TAG_CHARACTER_LIMIT, 1.0),
        text=f"{used} / {TAG_CHARACTER_LIMIT} tag characters used",
    )
    st.markdown(" ".join(f"`{k}`" for k in video.keywords))
    st.caption("Comma-separated (copy icon on the right):")
    st.code(", ".join(video.keywords), language=None)
    tags = pd.DataFrame({"tag": video.keywords, "characters": [len(k) for k in video.keywords]})
    st.download_button(
        "⬇️ Download tags (.csv)", tags.to_csv(index=False), file_name=f"{video.video_id}_tags.csv"
    )
else:
    st.warning("This video has no public tags.")

if video.hashtags:
    st.subheader("#️⃣ Hashtags in description")
    st.code(" ".join(video.hashtags), language=None)

if video.description:
    with st.expander("Description"):
        st.text(video.description)

st.divider()
st.caption("Built by [Faizan Saleem Siddiqui](https://github.com/FaizanSSDQ)")
