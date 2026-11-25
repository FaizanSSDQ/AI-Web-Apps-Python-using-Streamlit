"""
URL Shortener - Streamlit UI.

Run:  streamlit run app.py

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

from datetime import datetime

import pandas as pd
import streamlit as st

from shortener import PROVIDERS, make_qr_png, normalize_url, savings, shorten

st.set_page_config(page_title="URL Shortener", page_icon="🔗", layout="centered")
st.title("🔗 URL Shortener")
st.caption(
    "Turn long links into short ones, with a QR code, using free public shortening services."
)

history: list[dict] = st.session_state.setdefault("history", [])

with st.form("shorten_form"):
    long_url = st.text_input(
        "Long URL", placeholder="https://www.example.com/a/very/long/link?with=parameters"
    )
    provider = st.selectbox("Service", list(PROVIDERS))
    submitted = st.form_submit_button("Shorten", type="primary")

if submitted:
    try:
        clean = normalize_url(long_url)
        with st.spinner(f"Contacting {provider}..."):
            short = shorten(clean, provider)
        history.insert(
            0,
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "service": provider,
                "short": short,
                "original": clean,
            },
        )
        del history[10:]
    except ValueError as exc:
        st.error(str(exc))
    except Exception as exc:  # network errors / provider rejected the URL
        st.error(f"{provider} could not shorten this URL. Try another service. ({exc})")

if history:
    latest = history[0]
    st.success("Short link ready. Use the copy icon on the right of the box.")
    st.code(latest["short"], language=None)
    c1, c2 = st.columns(2)
    c1.metric("Characters saved", f"{savings(latest['original'], latest['short'])} %")
    c2.link_button("Open link ↗", latest["short"])

    qr = make_qr_png(latest["short"])
    q1, q2 = st.columns([1, 2])
    q1.image(qr, caption="QR code", width=180)
    q2.download_button("⬇️ Download QR code (PNG)", qr, file_name="qr_code.png", mime="image/png")

    with st.expander(f"History ({len(history)})"):
        table = pd.DataFrame(history)
        st.dataframe(table, hide_index=True)
        st.download_button(
            "⬇️ Export history (.csv)", table.to_csv(index=False), file_name="short_links.csv"
        )

st.divider()
st.caption("Built by [Faizan Saleem Siddiqui](https://github.com/FaizanSSDQ)")
