"""
YouTube Keyword Extractor - video ID parsing and metadata extraction.

Reads the public watch page and extracts the video's tags (keywords), title,
channel, views, duration, category and hashtags. Primary source is the
``ytInitialPlayerResponse`` JSON embedded in the page; HTML meta tags are a fallback.

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
TAG_CHARACTER_LIMIT = 500  # YouTube's limit for the tags field
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
CONSENT_COOKIES = {"CONSENT": "YES+cb", "SOCS": "CAI"}  # skip the EU consent page


@dataclass
class VideoInfo:
    video_id: str
    title: str = ""
    channel: str = ""
    keywords: list[str] = field(default_factory=list)
    description: str = ""
    views: int | None = None
    length_seconds: int | None = None
    category: str = ""
    publish_date: str = ""

    @property
    def thumbnail_url(self) -> str:
        return f"https://i.ytimg.com/vi/{self.video_id}/hqdefault.jpg"

    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.video_id}"

    @property
    def hashtags(self) -> list[str]:
        return list(dict.fromkeys(re.findall(r"#\w+", self.description)))

    @property
    def tags_character_count(self) -> int:
        return len(",".join(self.keywords))


def extract_video_id(value: str) -> str:
    """Accept a bare ID or any common YouTube URL form and return the 11-char video ID."""
    value = value.strip()
    if VIDEO_ID_RE.match(value):
        return value
    if not re.match(r"^https?://", value):
        value = "https://" + value
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower().removeprefix("www.").removeprefix("m.")
    candidate = ""
    if host == "youtu.be":
        candidate = parsed.path.lstrip("/").split("/")[0]
    elif host in ("youtube.com", "music.youtube.com", "youtube-nocookie.com"):
        if parsed.path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [""])[0]
        else:
            parts = parsed.path.strip("/").split("/")
            if len(parts) >= 2 and parts[0] in ("shorts", "embed", "live", "v"):
                candidate = parts[1]
    if not VIDEO_ID_RE.match(candidate):
        raise ValueError("Could not find a YouTube video ID in that link.")
    return candidate


def _json_after(html: str, marker: str) -> dict | None:
    """Decode the JSON object that follows ``marker`` in the page source."""
    index = html.find(marker)
    if index == -1:
        return None
    start = html.find("{", index)
    try:
        obj, _ = json.JSONDecoder().raw_decode(html, start)
        return obj
    except ValueError:
        return None


def parse_video_page(html: str, video_id: str) -> VideoInfo:
    info = VideoInfo(video_id=video_id)
    player = _json_after(html, "ytInitialPlayerResponse =") or _json_after(
        html, "ytInitialPlayerResponse="
    )

    if player and "videoDetails" in player:
        details = player["videoDetails"]
        micro = player.get("microformat", {}).get("playerMicroformatRenderer", {})
        info.title = details.get("title", "")
        info.channel = details.get("author", "")
        info.keywords = list(dict.fromkeys(details.get("keywords", [])))
        info.description = details.get("shortDescription", "")
        info.views = (
            int(details["viewCount"]) if str(details.get("viewCount", "")).isdigit() else None
        )
        info.length_seconds = (
            int(details["lengthSeconds"])
            if str(details.get("lengthSeconds", "")).isdigit()
            else None
        )
        info.category = micro.get("category", "")
        info.publish_date = micro.get("publishDate", "")[:10]
        return info

    # Fallback: classic meta tags
    soup = BeautifulSoup(html, "lxml")

    def meta(**attrs: str) -> str:
        tag = soup.find("meta", attrs=attrs)
        return tag["content"].strip() if tag and tag.get("content") else ""

    info.title = meta(name="title") or meta(property="og:title")
    info.description = meta(name="description") or meta(property="og:description")
    keywords = meta(name="keywords")
    info.keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    if not info.title and not info.keywords:
        raise ValueError(
            "Video metadata not found (the video may be private, removed or age-restricted)."
        )
    return info


def fetch_video_info(
    url_or_id: str, session: requests.Session | None = None, timeout: float = 15.0
) -> VideoInfo:
    video_id = extract_video_id(url_or_id)
    http = session or requests.Session()
    response = http.get(
        "https://www.youtube.com/watch",
        params={"v": video_id, "hl": "en"},
        headers=HEADERS,
        cookies=CONSENT_COOKIES,
        timeout=timeout,
    )
    response.raise_for_status()
    return parse_video_page(response.text, video_id)


def format_duration(seconds: int | None) -> str:
    if seconds is None:
        return "-"
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes}:{secs:02d}"
