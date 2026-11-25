"""
Audio-to-Text Converter - transcription engine.

Pipeline: decode audio -> detect speech regions (silence-based segmentation)
-> transcribe each region with the Google Web Speech API -> join the text.

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

from __future__ import annotations

import io
import math
from collections.abc import Callable
from dataclasses import dataclass

import speech_recognition as sr
from pydub import AudioSegment, silence

SUPPORTED_FORMATS = ("wav", "mp3", "m4a", "ogg", "flac", "webm")

LANGUAGES = {
    "English (US)": "en-US",
    "English (UK)": "en-GB",
    "Urdu": "ur-PK",
    "Arabic": "ar-SA",
    "German": "de-DE",
    "French": "fr-FR",
    "Spanish": "es-ES",
}


@dataclass(frozen=True)
class SplitSettings:
    """Parameters for silence-based segmentation."""

    min_silence_ms: int = 500  # a pause at least this long splits the audio
    silence_offset_db: float = 16.0  # silence threshold = average loudness - offset
    keep_silence_ms: int = 200  # padding kept around each speech region
    max_chunk_ms: int = 50_000  # the free API rejects very long requests


@dataclass(frozen=True)
class ChunkResult:
    index: int
    start_ms: int
    end_ms: int
    text: str
    recognized: bool


def load_audio(data: bytes, filename: str) -> AudioSegment:
    """Decode raw bytes into an AudioSegment (non-WAV formats need ffmpeg)."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else None
    return AudioSegment.from_file(io.BytesIO(data), format=ext)


def split_audio(
    audio: AudioSegment, settings: SplitSettings | None = None
) -> list[tuple[int, int]]:
    """Return (start_ms, end_ms) ranges that contain speech."""
    settings = settings or SplitSettings()
    if len(audio) == 0 or math.isinf(audio.dBFS):
        return []  # empty or fully silent

    ranges = silence.detect_nonsilent(
        audio,
        min_silence_len=settings.min_silence_ms,
        silence_thresh=audio.dBFS - settings.silence_offset_db,
    )

    chunks: list[tuple[int, int]] = []
    for start, end in ranges:
        start = max(0, start - settings.keep_silence_ms)
        end = min(len(audio), end + settings.keep_silence_ms)
        while end - start > settings.max_chunk_ms:
            chunks.append((start, start + settings.max_chunk_ms))
            start += settings.max_chunk_ms
        chunks.append((start, end))
    return chunks


def transcribe_segment(segment: AudioSegment, recognizer: sr.Recognizer, language: str) -> str:
    """Transcribe a single in-memory segment (no temporary files)."""
    buffer = io.BytesIO()
    segment.set_channels(1).export(buffer, format="wav")
    buffer.seek(0)
    with sr.AudioFile(buffer) as source:
        audio_data = recognizer.record(source)
    return recognizer.recognize_google(audio_data, language=language)


def transcribe(
    audio: AudioSegment,
    ranges: list[tuple[int, int]],
    language: str = "en-US",
    recognizer: sr.Recognizer | None = None,
    on_progress: Callable[[int, int], None] | None = None,
) -> list[ChunkResult]:
    """Transcribe every range. Unintelligible chunks are kept as empty results.

    Network/API failures (``sr.RequestError``) are raised to the caller.
    """
    recognizer = recognizer or sr.Recognizer()
    results: list[ChunkResult] = []
    for index, (start, end) in enumerate(ranges):
        try:
            text = transcribe_segment(audio[start:end], recognizer, language).strip()
            recognized = bool(text)
        except sr.UnknownValueError:
            text, recognized = "", False
        results.append(ChunkResult(index, start, end, text, recognized))
        if on_progress:
            on_progress(index + 1, len(ranges))
    return results


def format_timestamp(ms: int) -> str:
    seconds = ms // 1000
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def build_transcript(results: list[ChunkResult], timestamps: bool = False) -> str:
    """Join chunk texts into a readable transcript."""
    recognized = [r for r in results if r.recognized]
    if timestamps:
        return "\n".join(
            f"[{format_timestamp(r.start_ms)} - {format_timestamp(r.end_ms)}] {r.text.capitalize()}"
            for r in recognized
        )
    return " ".join(r.text.capitalize() for r in recognized)
