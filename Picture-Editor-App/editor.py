"""
Picture Editor - image processing engine (Pillow).

All edits are described by an ``EditSettings`` object and applied in a fixed,
predictable order: crop -> resize -> rotate -> flip -> adjust -> filter.
Transparency (alpha channel) is preserved throughout.

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

from __future__ import annotations

import io
from collections.abc import Callable
from dataclasses import dataclass

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

FILTERS = (
    "None",
    "Grayscale",
    "Sepia",
    "Invert",
    "Blur",
    "Gaussian blur",
    "Sharpen",
    "Detail",
    "Edge enhance",
    "Find edges",
    "Emboss",
    "Contour",
    "Smooth",
)
EXPORT_FORMATS = ("PNG", "JPEG", "WEBP")


@dataclass
class EditSettings:
    crop_left: int = 0  # margins in percent of width / height
    crop_top: int = 0
    crop_right: int = 0
    crop_bottom: int = 0
    width: int | None = None
    height: int | None = None
    rotate: float = 0.0  # degrees, counter-clockwise
    flip_horizontal: bool = False
    flip_vertical: bool = False
    brightness: float = 1.0
    contrast: float = 1.0
    saturation: float = 1.0
    sharpness: float = 1.0
    filter: str = "None"
    blur_radius: float = 2.0


def normalize(img: Image.Image) -> Image.Image:
    """Apply EXIF orientation and convert to RGB or RGBA."""
    img = ImageOps.exif_transpose(img)
    has_alpha = img.mode in ("RGBA", "LA", "PA") or (img.mode == "P" and "transparency" in img.info)
    return img.convert("RGBA" if has_alpha else "RGB")


def _on_rgb(img: Image.Image, fn: Callable[[Image.Image], Image.Image]) -> Image.Image:
    """Run ``fn`` on the colour channels only, keeping the alpha channel untouched."""
    if img.mode != "RGBA":
        return fn(img).convert("RGB")
    alpha = img.getchannel("A")
    out = fn(img.convert("RGB")).convert("RGB")
    out.putalpha(alpha)
    return out


def _sepia(img: Image.Image) -> Image.Image:
    return ImageOps.colorize(ImageOps.grayscale(img), black="#2b1d0e", white="#f5e6c8")


FILTER_FUNCTIONS: dict[str, Callable[[Image.Image, EditSettings], Image.Image]] = {
    "Grayscale": lambda im, s: ImageOps.grayscale(im),
    "Sepia": lambda im, s: _sepia(im),
    "Invert": lambda im, s: ImageOps.invert(im),
    "Blur": lambda im, s: im.filter(ImageFilter.BLUR),
    "Gaussian blur": lambda im, s: im.filter(ImageFilter.GaussianBlur(s.blur_radius)),
    "Sharpen": lambda im, s: im.filter(ImageFilter.SHARPEN),
    "Detail": lambda im, s: im.filter(ImageFilter.DETAIL),
    "Edge enhance": lambda im, s: im.filter(ImageFilter.EDGE_ENHANCE_MORE),
    "Find edges": lambda im, s: im.filter(ImageFilter.FIND_EDGES),
    "Emboss": lambda im, s: im.filter(ImageFilter.EMBOSS),
    "Contour": lambda im, s: im.filter(ImageFilter.CONTOUR),
    "Smooth": lambda im, s: im.filter(ImageFilter.SMOOTH_MORE),
}


def apply_edits(img: Image.Image, s: EditSettings) -> Image.Image:
    img = normalize(img)

    # 1. crop (percent margins)
    if any((s.crop_left, s.crop_top, s.crop_right, s.crop_bottom)):
        w, h = img.size
        box = (
            round(w * s.crop_left / 100),
            round(h * s.crop_top / 100),
            w - round(w * s.crop_right / 100),
            h - round(h * s.crop_bottom / 100),
        )
        if box[2] - box[0] < 1 or box[3] - box[1] < 1:
            raise ValueError("Crop margins remove the whole image.")
        img = img.crop(box)

    # 2. resize
    if s.width and s.height and (s.width, s.height) != img.size:
        img = img.resize((int(s.width), int(s.height)), Image.Resampling.LANCZOS)

    # 3. rotate (canvas grows to fit; new corners are white or transparent)
    if s.rotate % 360:
        fill = (0, 0, 0, 0) if img.mode == "RGBA" else (255, 255, 255)
        img = img.rotate(s.rotate, expand=True, resample=Image.Resampling.BICUBIC, fillcolor=fill)

    # 4. flip
    if s.flip_horizontal:
        img = ImageOps.mirror(img)
    if s.flip_vertical:
        img = ImageOps.flip(img)

    # 5. tone adjustments
    for factor, enhancer in (
        (s.brightness, ImageEnhance.Brightness),
        (s.contrast, ImageEnhance.Contrast),
        (s.saturation, ImageEnhance.Color),
        (s.sharpness, ImageEnhance.Sharpness),
    ):
        if factor != 1.0:
            img = _on_rgb(img, lambda im, e=enhancer, f=factor: e(im).enhance(f))

    # 6. filter
    if s.filter != "None":
        if s.filter not in FILTER_FUNCTIONS:
            raise ValueError(f"Unknown filter: {s.filter}")
        img = _on_rgb(img, lambda im: FILTER_FUNCTIONS[s.filter](im, s))

    return img


def to_bytes(img: Image.Image, fmt: str = "PNG", quality: int = 90) -> bytes:
    """Encode for download. JPEG has no transparency, so alpha is flattened onto white."""
    fmt = fmt.upper()
    if fmt not in EXPORT_FORMATS:
        raise ValueError(f"Unsupported export format: {fmt}")
    if fmt == "JPEG" and img.mode == "RGBA":
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.getchannel("A"))
        img = background
    buffer = io.BytesIO()
    options = {"quality": quality} if fmt in ("JPEG", "WEBP") else {"optimize": True}
    img.save(buffer, format=fmt, **options)
    return buffer.getvalue()
