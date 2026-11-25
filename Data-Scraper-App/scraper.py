"""
Web Data Scraper - extraction engine.

Fetches a web page and extracts structured data: metadata, headings, links,
images, HTML tables (as DataFrames) and readable text.

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

from __future__ import annotations

import io
import re
import zipfile
from collections.abc import Callable
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp")


@dataclass
class PageData:
    url: str
    title: str = ""
    description: str = ""
    headings: list[dict] = field(default_factory=list)
    links: list[dict] = field(default_factory=list)
    images: list[dict] = field(default_factory=list)
    tables: list[pd.DataFrame] = field(default_factory=list)
    text: str = ""

    @property
    def word_count(self) -> int:
        return len(self.text.split())


def normalize_url(url: str) -> str:
    """Add a scheme if missing and validate the result."""
    url = url.strip()
    if not url:
        raise ValueError("Please enter a URL.")
    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = "https://" + url
    parsed = urlparse(url)
    if not parsed.netloc or "." not in parsed.netloc:
        raise ValueError(f"'{url}' is not a valid web address.")
    return url


def fetch_html(
    url: str, timeout: float = 15.0, session: requests.Session | None = None
) -> tuple[str, str]:
    """Download a page. Returns (final_url, html)."""
    http = session or requests.Session()
    response = http.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "")
    if "html" not in content_type and "xml" not in content_type:
        raise ValueError(f"The URL returned '{content_type or 'unknown'}', not an HTML page.")
    return response.url, response.text


def parse_page(html: str, base_url: str) -> PageData:
    """Extract structured data from HTML."""
    soup = BeautifulSoup(html, "lxml")
    base_host = urlparse(base_url).netloc
    page = PageData(url=base_url)

    if soup.title and soup.title.string:
        page.title = soup.title.string.strip()
    description = soup.find("meta", attrs={"name": "description"}) or soup.find(
        "meta", attrs={"property": "og:description"}
    )
    if description and description.get("content"):
        page.description = description["content"].strip()

    for tag in soup.find_all(["h1", "h2", "h3", "h4"]):
        text = tag.get_text(" ", strip=True)
        if text:
            page.headings.append({"level": tag.name.upper(), "text": text})

    seen: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if href.startswith(("#", "javascript:")):
            continue
        absolute = urljoin(base_url, href)
        if absolute in seen:
            continue
        seen.add(absolute)
        scheme = urlparse(absolute).scheme
        page.links.append(
            {
                "text": anchor.get_text(" ", strip=True)[:120],
                "url": absolute,
                "type": "email"
                if scheme == "mailto"
                else ("internal" if urlparse(absolute).netloc == base_host else "external"),
            }
        )

    seen.clear()
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
        if not src or src.startswith("data:"):
            continue
        absolute = urljoin(base_url, src.strip())
        if absolute in seen:
            continue
        seen.add(absolute)
        page.images.append({"url": absolute, "alt": (img.get("alt") or "").strip()})

    try:
        page.tables = pd.read_html(io.StringIO(html))
    except ValueError:  # no <table> elements
        page.tables = []

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    page.text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True)).strip()
    return page


def scrape(url: str, session: requests.Session | None = None) -> PageData:
    final_url, html = fetch_html(normalize_url(url), session=session)
    return parse_page(html, final_url)


def _safe_filename(url: str, index: int) -> str:
    name = urlparse(url).path.rsplit("/", 1)[-1] or f"image_{index}"
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)[:80]
    if not name.lower().endswith(IMAGE_EXTENSIONS):
        name += ".jpg"
    return f"{index:03d}_{name}"


def build_image_zip(
    urls: list[str], fetch: Callable[[str], bytes], limit: int = 50
) -> tuple[bytes, int]:
    """Download up to ``limit`` images into a ZIP. Returns (zip_bytes, saved_count)."""
    buffer = io.BytesIO()
    saved = 0
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for index, url in enumerate(urls[:limit], start=1):
            try:
                archive.writestr(_safe_filename(url, index), fetch(url))
                saved += 1
            except Exception:  # skip broken or blocked images
                continue
    return buffer.getvalue(), saved


def http_fetch_bytes(url: str, timeout: float = 15.0) -> bytes:
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    response.raise_for_status()
    return response.content
