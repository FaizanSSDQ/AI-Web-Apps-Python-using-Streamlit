"""Tests for the transcription engine (no network: the recognizer is faked)."""

import speech_recognition as sr
from pydub import AudioSegment
from pydub.generators import Sine

from transcriber import (
    ChunkResult,
    SplitSettings,
    build_transcript,
    format_timestamp,
    split_audio,
    transcribe,
)


def make_speech_like_audio() -> AudioSegment:
    """1 s tone, 1 s silence, 1 s tone."""
    tone = Sine(440).to_audio_segment(duration=1000).apply_gain(-6)
    gap = AudioSegment.silent(duration=1000)
    return tone + gap + tone


def test_split_finds_two_regions():
    ranges = split_audio(make_speech_like_audio(), SplitSettings(keep_silence_ms=0))
    assert len(ranges) == 2
    assert ranges[0][0] == 0
    assert 900 <= ranges[1][0] <= 2100


def test_split_on_silence_returns_nothing():
    assert split_audio(AudioSegment.silent(duration=2000)) == []
    assert split_audio(AudioSegment.empty()) == []


def test_split_respects_max_chunk_length():
    tone = Sine(440).to_audio_segment(duration=5000)
    ranges = split_audio(tone, SplitSettings(max_chunk_ms=2000, keep_silence_ms=0))
    assert all(end - start <= 2000 for start, end in ranges)
    assert ranges[-1][1] == 5000


class FakeRecognizer(sr.Recognizer):
    def __init__(self, replies):
        super().__init__()
        self.replies = list(replies)

    def recognize_google(self, audio_data, language="en-US", **kwargs):
        reply = self.replies.pop(0)
        if reply is None:
            raise sr.UnknownValueError()
        return reply


def test_transcribe_joins_and_tracks_progress():
    audio = make_speech_like_audio()
    ranges = split_audio(audio)
    progress = []
    results = transcribe(
        audio,
        ranges,
        recognizer=FakeRecognizer(["hello world", None]),
        on_progress=lambda d, t: progress.append((d, t)),
    )
    assert [r.recognized for r in results] == [True, False]
    assert progress == [(1, 2), (2, 2)]
    assert build_transcript(results) == "Hello world"


def test_build_transcript_with_timestamps():
    results = [ChunkResult(0, 0, 61_000, "first part", True)]
    assert build_transcript(results, timestamps=True) == "[00:00 - 01:01] First part"


def test_format_timestamp():
    assert format_timestamp(125_400) == "02:05"
