"""Tests for the image processing engine."""

import io

import pytest
from PIL import Image

from editor import FILTERS, EditSettings, apply_edits, normalize, to_bytes


@pytest.fixture
def rgb():
    img = Image.new("RGB", (200, 100), (200, 50, 50))
    img.paste((20, 120, 220), (100, 0, 200, 100))  # right half blue
    return img


@pytest.fixture
def rgba():
    img = Image.new("RGBA", (64, 64), (255, 0, 0, 255))
    img.paste((0, 0, 0, 0), (0, 0, 32, 64))  # left half transparent
    return img


def test_no_edits_returns_same_pixels(rgb):
    assert apply_edits(rgb, EditSettings()).tobytes() == rgb.tobytes()


def test_crop_resize_rotate_order(rgb):
    out = apply_edits(rgb, EditSettings(crop_left=50, width=50, height=100, rotate=90))
    assert out.size == (100, 50)  # cropped to 100x100, resized to 50x100, rotated 90°
    assert out.getpixel((50, 25))[2] > 200  # only the blue half remains


def test_flip_horizontal(rgb):
    out = apply_edits(rgb, EditSettings(flip_horizontal=True))
    assert out.getpixel((0, 0)) == (20, 120, 220)


def test_crop_everything_raises(rgb):
    with pytest.raises(ValueError):
        apply_edits(rgb, EditSettings(crop_left=50, crop_right=50))


@pytest.mark.parametrize("name", FILTERS)
@pytest.mark.parametrize("fixture", ["rgb", "rgba"])
def test_every_filter_runs_and_keeps_mode(name, fixture, request):
    img = request.getfixturevalue(fixture)
    out = apply_edits(img, EditSettings(filter=name))
    assert out.mode == img.mode
    assert out.size == img.size


def test_alpha_is_preserved_by_adjustments(rgba):
    out = apply_edits(rgba, EditSettings(brightness=0.3, contrast=1.5, filter="Sepia"))
    assert out.getpixel((10, 10))[3] == 0
    assert out.getpixel((50, 10))[3] == 255


def test_grayscale_pixels_are_neutral(rgb):
    r, g, b = apply_edits(rgb, EditSettings(filter="Grayscale")).getpixel((10, 10))
    assert r == g == b


def test_normalize_converts_palette_images():
    assert normalize(Image.new("P", (4, 4))).mode == "RGB"
    assert normalize(Image.new("LA", (4, 4))).mode == "RGBA"


@pytest.mark.parametrize("fmt", ["PNG", "JPEG", "WEBP"])
def test_export_formats(rgba, fmt):
    data = to_bytes(rgba, fmt)
    assert Image.open(io.BytesIO(data)).format == fmt


def test_unknown_export_format(rgb):
    with pytest.raises(ValueError):
        to_bytes(rgb, "TIFF")
