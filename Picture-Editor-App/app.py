"""
Picture Editor - Streamlit UI with live preview.

Run:  streamlit run app.py

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

import streamlit as st
from PIL import Image, UnidentifiedImageError

from editor import EXPORT_FORMATS, FILTERS, EditSettings, apply_edits, normalize, to_bytes

st.set_page_config(page_title="Picture Editor", page_icon="🎨", layout="wide")
st.title("🎨 Picture Editor")
st.caption("Crop, resize, rotate, adjust and filter images with a live before/after preview.")

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp", "bmp"])
if uploaded is None:
    st.info("Upload a JPG, PNG, WebP or BMP image to start editing.")
    st.stop()

try:
    original = normalize(Image.open(uploaded))
except UnidentifiedImageError:
    st.error("This file is not a valid image.")
    st.stop()

CONTROL_KEYS = (
    "crop_l",
    "crop_t",
    "crop_r",
    "crop_b",
    "keep_ratio",
    "width",
    "height",
    "rotate",
    "flip_h",
    "flip_v",
    "brightness",
    "contrast",
    "saturation",
    "sharpness",
    "filter",
    "radius",
)


def reset_controls() -> None:
    for key in CONTROL_KEYS:
        st.session_state.pop(key, None)


with st.sidebar:
    st.header("Edit")
    st.button("↺ Reset all edits", on_click=reset_controls)

    with st.expander("✂️ Crop (margins %)", expanded=False):
        crop_l = st.slider("Left", 0, 45, 0, key="crop_l")
        crop_r = st.slider("Right", 0, 45, 0, key="crop_r")
        crop_t = st.slider("Top", 0, 45, 0, key="crop_t")
        crop_b = st.slider("Bottom", 0, 45, 0, key="crop_b")

    cropped_w = max(1, round(original.width * (100 - crop_l - crop_r) / 100))
    cropped_h = max(1, round(original.height * (100 - crop_t - crop_b) / 100))

    with st.expander("📐 Resize & rotate", expanded=True):
        keep_ratio = st.checkbox("Keep aspect ratio", value=True, key="keep_ratio")
        width = st.number_input("Width (px)", 1, 8000, cropped_w, key="width")
        if keep_ratio:
            height = max(1, round(width * cropped_h / cropped_w))
            st.caption(f"Height: {height} px")
        else:
            height = st.number_input("Height (px)", 1, 8000, cropped_h, key="height")
        rotate = st.slider("Rotate (° counter-clockwise)", -180, 180, 0, key="rotate")
        flip_h = st.checkbox("Flip horizontally", key="flip_h")
        flip_v = st.checkbox("Flip vertically", key="flip_v")

    with st.expander("🌗 Adjust", expanded=True):
        brightness = st.slider("Brightness", 0.0, 2.0, 1.0, 0.05, key="brightness")
        contrast = st.slider("Contrast", 0.0, 2.0, 1.0, 0.05, key="contrast")
        saturation = st.slider("Saturation", 0.0, 2.0, 1.0, 0.05, key="saturation")
        sharpness = st.slider("Sharpness", 0.0, 3.0, 1.0, 0.1, key="sharpness")

    with st.expander("✨ Filter", expanded=True):
        filter_name = st.selectbox("Filter", FILTERS, key="filter")
        radius = 2.0
        if filter_name == "Gaussian blur":
            radius = st.slider("Blur radius", 0.5, 15.0, 2.0, 0.5, key="radius")

settings = EditSettings(
    crop_left=crop_l,
    crop_top=crop_t,
    crop_right=crop_r,
    crop_bottom=crop_b,
    width=int(width),
    height=int(height),
    rotate=rotate,
    flip_horizontal=flip_h,
    flip_vertical=flip_v,
    brightness=brightness,
    contrast=contrast,
    saturation=saturation,
    sharpness=sharpness,
    filter=filter_name,
    blur_radius=radius,
)

try:
    edited = apply_edits(original, settings)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

before, after = st.columns(2)
with before:
    st.subheader("Original")
    st.image(original, width="stretch")
    st.caption(
        f"{original.width} × {original.height} px · {Image.open(uploaded).format} · {original.mode}"
    )
with after:
    st.subheader("Edited")
    st.image(edited, width="stretch")
    st.caption(f"{edited.width} × {edited.height} px · {edited.mode}")

st.subheader("Export")
e1, e2, e3 = st.columns([1, 2, 2])
fmt = e1.selectbox("Format", EXPORT_FORMATS)
quality = e2.slider("Quality", 50, 100, 90, disabled=fmt == "PNG")
stem = uploaded.name.rsplit(".", 1)[0]
e3.download_button(
    f"⬇️ Download {fmt}",
    data=to_bytes(edited, fmt, quality),
    file_name=f"{stem}_edited.{fmt.lower().replace('jpeg', 'jpg')}",
    mime=f"image/{fmt.lower()}",
)

st.divider()
st.caption("Built by [Faizan Saleem Siddiqui](https://github.com/FaizanSSDQ)")
