"""
URL Shortener - validation, shortening and QR code generation.

Uses public, key-free shortening services through ``pyshorteners``.

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

from __future__ import annotations

import io
import re
from urllib.parse import urlparse

import pyshorteners
import qrcode
from qrcode.constants import ERROR_CORRECT_M

# display name -> pyshorteners attribute
PROVIDERS = {"TinyURL": "tinyurl", "da.gd": "dagd", "clck.ru": "clckru"}


def normalize_url(url: str) -> str:
    """Validate a URL and add https:// if no scheme is given."""
    url = url.strip()
    if not url:
        raise ValueError("Please enter a URL.")
    if " " in url:
        raise ValueError("URLs cannot contain spaces.")
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "https://" + url
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http and https links can be shortened.")
    host = parsed.hostname or ""
    if "." not in host or host.startswith(".") or host.endswith("."):
        raise ValueError(f"'{url}' does not look like a valid web address.")
    return url


def shorten(url: str, provider: str = "TinyURL", client=None, timeout: int = 10) -> str:
    """Shorten ``url`` with the given provider. ``client`` can be injected for testing."""
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider}")
    client = client or pyshorteners.Shortener(timeout=timeout)
    return getattr(client, PROVIDERS[provider]).short(normalize_url(url))


def make_qr_png(
    data: str, box_size: int = 10, border: int = 2, fill: str = "black", background: str = "white"
) -> bytes:
    """Return a PNG QR code for ``data``."""
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill_color=fill, back_color=background)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def savings(original: str, short: str) -> int:
    """Characters saved, as a percentage of the original length."""
    return max(0, round(100 * (len(original) - len(short)) / len(original))) if original else 0
