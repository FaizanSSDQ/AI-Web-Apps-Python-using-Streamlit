"""
Audio-to-Text Converter - Streamlit UI.

Run:  streamlit run app.py

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

import speech_recognition as sr
import streamlit as st

from transcriber import (
    LANGUAGES,
    SUPPORTED_FORMATS,
    SplitSettings,
    build_transcript,
    load_audio,
    split_audio,
    transcribe,
)

st.set_page_config(page_title="Audio to Text Converter", page_icon="🎙️", layout="wide")
st.title("🎙️ Audio to Text Converter")
st.caption(
    "Upload a recording. It is split into speech segments on silence, and each segment "
    "is transcribed with the Google Web Speech API."
)

with st.sidebar:
    st.header("Settings")
    language_name = st.selectbox("Spoken language", list(LANGUAGES))
    show_timestamps = st.checkbox("Include timestamps", value=False)
    with st.expander("Segmentation (advanced)"):
        min_silence = st.slider("Minimum pause (ms)", 200, 2000, 500, step=100)
        offset_db = st.slider("Silence threshold below average (dB)", 6, 30, 16)
        keep_silence = st.slider("Padding around speech (ms)", 0, 1000, 200, step=50)

uploaded = st.file_uploader("Upload an audio file", type=list(SUPPORTED_FORMATS))
if uploaded is None:
    st.info(f"Supported formats: {', '.join(SUPPORTED_FORMATS)}. WAV works without ffmpeg.")
    st.stop()

st.audio(uploaded)

try:
    audio = load_audio(uploaded.getvalue(), uploaded.name)
except Exception as exc:  # pydub raises several decoder-specific errors
    st.error(f"Could not decode this file. Non-WAV formats need ffmpeg installed. ({exc})")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Duration", f"{len(audio) / 1000:.1f} s")
c2.metric("Sample rate", f"{audio.frame_rate} Hz")
c3.metric("Channels", audio.channels)

file_key = f"{uploaded.name}:{uploaded.size}"
if st.button("Transcribe", type="primary"):
    settings = SplitSettings(
        min_silence_ms=min_silence, silence_offset_db=offset_db, keep_silence_ms=keep_silence
    )
    ranges = split_audio(audio, settings)
    if not ranges:
        st.warning("No speech detected. Try lowering the silence threshold.")
        st.stop()

    progress = st.progress(0.0, text="Transcribing...")
    try:
        results = transcribe(
            audio,
            ranges,
            language=LANGUAGES[language_name],
            on_progress=lambda done, total: progress.progress(
                done / total, text=f"Segment {done} of {total}"
            ),
        )
    except sr.RequestError as exc:
        st.error(f"Speech API request failed (check your internet connection): {exc}")
        st.stop()
    progress.empty()
    st.session_state["transcription"] = (file_key, results)

stored = st.session_state.get("transcription")
if stored and stored[0] == file_key:
    results = stored[1]
    transcript = build_transcript(results, timestamps=show_timestamps)
    recognized = sum(r.recognized for r in results)

    st.subheader("Transcript")
    m1, m2 = st.columns(2)
    m1.metric("Words", len(transcript.split()))
    m2.metric("Segments recognised", f"{recognized} / {len(results)}")

    edited = st.text_area("You can correct the text before downloading", transcript, height=250)
    st.download_button(
        "⬇️ Download transcript (.txt)",
        data=edited,
        file_name=f"{uploaded.name.rsplit('.', 1)[0]}_transcript.txt",
        mime="text/plain",
    )

st.divider()
st.caption("Built by [Faizan Saleem Siddiqui](https://github.com/FaizanSSDQ)")
