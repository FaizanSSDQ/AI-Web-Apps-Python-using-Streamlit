"""Tests for video ID parsing and metadata extraction (offline: synthetic pages)."""

import json

import pytest

from youtube import extract_video_id, format_duration, parse_video_page

VID = "dQw4w9WgXcQ"


@pytest.mark.parametrize(
    "link",
    [
        VID,
        f"https://www.youtube.com/watch?v={VID}",
        f"https://www.youtube.com/watch?feature=share&v={VID}&t=42",
        f"youtube.com/watch?v={VID}",
        f"https://m.youtube.com/watch?v={VID}",
        f"https://youtu.be/{VID}?si=abc",
        f"https://www.youtube.com/shorts/{VID}",
        f"https://www.youtube.com/embed/{VID}",
        f"https://www.youtube.com/live/{VID}?feature=share",
        f"https://music.youtube.com/watch?v={VID}",
    ],
)
def test_extract_video_id(link):
    assert extract_video_id(link) == VID


@pytest.mark.parametrize(
    "bad", ["", "https://vimeo.com/123", "https://youtube.com/channel/xyz", "short"]
)
def test_extract_video_id_rejects(bad):
    with pytest.raises(ValueError):
        extract_video_id(bad)


def player_page(details: dict) -> str:
    response = {
        "videoDetails": details,
        "microformat": {
            "playerMicroformatRenderer": {
                "category": "Science & Technology",
                "publishDate": "2025-03-01T00:00:00-08:00",
            }
        },
    }
    # braces inside strings must not confuse the parser
    return f"<script>var ytInitialPlayerResponse = {json.dumps(response)};var meta = {{}};</script>"


def test_parse_player_response():
    html = player_page(
        {
            "title": "STM32 DMA {explained}",
            "author": "Embedded Lab",
            "keywords": ["stm32", "dma", "stm32", "firmware"],
            "shortDescription": "Learn DMA #stm32 #embedded #stm32",
            "viewCount": "12345",
            "lengthSeconds": "3725",
        }
    )
    info = parse_video_page(html, VID)
    assert info.title == "STM32 DMA {explained}"
    assert info.channel == "Embedded Lab"
    assert info.keywords == ["stm32", "dma", "firmware"]  # de-duplicated, order kept
    assert info.views == 12345
    assert format_duration(info.length_seconds) == "1:02:05"
    assert info.category == "Science & Technology"
    assert info.publish_date == "2025-03-01"
    assert info.hashtags == ["#stm32", "#embedded"]
    assert info.tags_character_count == len("stm32,dma,firmware")


def test_parse_falls_back_to_meta_tags():
    html = (
        '<html><head><meta name="title" content="ESP32 Radar">'
        '<meta name="keywords" content="esp32, radar , ultrasonic,"></head></html>'
    )
    info = parse_video_page(html, VID)
    assert info.title == "ESP32 Radar"
    assert info.keywords == ["esp32", "radar", "ultrasonic"]


def test_parse_raises_when_nothing_found():
    with pytest.raises(ValueError):
        parse_video_page("<html><body>Video unavailable</body></html>", VID)


def test_format_duration():
    assert format_duration(59) == "0:59"
    assert format_duration(None) == "-"
