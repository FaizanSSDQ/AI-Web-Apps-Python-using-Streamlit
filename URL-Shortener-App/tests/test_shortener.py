"""Tests for URL validation, shortening (fake client, no network) and QR codes."""

import io
from types import SimpleNamespace

import pytest
from PIL import Image

from shortener import PROVIDERS, make_qr_png, normalize_url, savings, shorten


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("example.com", "https://example.com"),
        ("  http://example.com/path?q=1 ", "http://example.com/path?q=1"),
        ("https://sub.domain.co.uk/x", "https://sub.domain.co.uk/x"),
    ],
)
def test_normalize_url_accepts(raw, expected):
    assert normalize_url(raw) == expected


@pytest.mark.parametrize(
    "bad", ["", "hello world", "ftp://files.example.com", "https://localhost", "abc"]
)
def test_normalize_url_rejects(bad):
    with pytest.raises(ValueError):
        normalize_url(bad)


def make_fake_client(calls):
    def service(name):
        return SimpleNamespace(
            short=lambda url: calls.append((name, url)) or f"https://{name}.test/abc"
        )

    return SimpleNamespace(**{attr: service(attr) for attr in PROVIDERS.values()})


@pytest.mark.parametrize("provider", list(PROVIDERS))
def test_shorten_uses_selected_provider(provider):
    calls = []
    short = shorten("example.com/page", provider, client=make_fake_client(calls))
    attr = PROVIDERS[provider]
    assert short == f"https://{attr}.test/abc"
    assert calls == [(attr, "https://example.com/page")]


def test_shorten_unknown_provider():
    with pytest.raises(ValueError):
        shorten("example.com", "bit.ly", client=make_fake_client([]))


def test_qr_code_is_valid_png():
    png = make_qr_png("https://tinyurl.com/abc")
    image = Image.open(io.BytesIO(png))
    assert image.format == "PNG"
    assert image.width == image.height > 100


def test_savings():
    assert savings("https://example.com/" + "x" * 80, "https://is.gd/abc") == 83
    assert savings("", "x") == 0
