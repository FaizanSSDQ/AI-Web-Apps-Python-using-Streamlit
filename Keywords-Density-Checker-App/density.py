"""
Keyword Density Checker - text analysis engine.

Computes word statistics, keyword / n-gram frequency and density, and
checks a target keyword against common SEO guidance.

Author : Faizan Saleem Siddiqui (https://github.com/FaizanSSDQ)
License: MIT
"""

from __future__ import annotations

import re
from collections import Counter

import pandas as pd
import requests
from bs4 import BeautifulSoup

STOPWORDS = frozenset(
    """
    a about above after again against all also am an and any are as at be because been before being
    below between both but by can could did do does doing down during each few for from further had
    has have having he her here hers herself him himself his how i if in into is it its itself just
    me more most my myself no nor not now of off on once only or other our ours ourselves out over
    own same she should so some such than that the their theirs them themselves then there these
    they this those through to too under until up very was we were what when where which while who
    whom why will with would you your yours yourself yourselves
    """.split()
)

WORD_RE = re.compile(r"[^\W_]+(?:['’-][^\W_]+)*", re.UNICODE)
SENTENCE_RE = re.compile(r"[.!?]+(?:\s|$)")
WORDS_PER_MINUTE = 200


def tokenize(text: str) -> list[str]:
    """Lower-case words; keeps contractions and hyphenated words together."""
    return [w.replace("’", "'") for w in WORD_RE.findall(text.lower())]


def text_stats(text: str) -> dict[str, float]:
    words = tokenize(text)
    sentences = max(1, len(SENTENCE_RE.findall(text.strip()))) if words else 0
    return {
        "words": len(words),
        "unique_words": len(set(words)),
        "sentences": sentences,
        "characters": len(text),
        "avg_words_per_sentence": round(len(words) / sentences, 1) if sentences else 0.0,
        "reading_time_min": round(len(words) / WORDS_PER_MINUTE, 1),
    }


def ngrams(tokens: list[str], n: int) -> list[tuple[str, ...]]:
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def _keep(gram: tuple[str, ...], remove_stopwords: bool, min_length: int) -> bool:
    if any(len(t) < min_length or t.isdigit() for t in gram):
        return False
    if remove_stopwords:
        # single words: drop stopwords; phrases: must not start or end with one
        if len(gram) == 1:
            return gram[0] not in STOPWORDS
        return gram[0] not in STOPWORDS and gram[-1] not in STOPWORDS
    return True


def keyword_density(
    text: str,
    n: int = 1,
    remove_stopwords: bool = True,
    min_length: int = 2,
    top_k: int | None = None,
) -> pd.DataFrame:
    """Frequency table: keyword, count, density % (occurrences per total words)."""
    tokens = tokenize(text)
    columns = ["keyword", "count", "density_%"]
    if not tokens:
        return pd.DataFrame(columns=columns)
    counts = Counter(
        " ".join(g) for g in ngrams(tokens, n) if _keep(g, remove_stopwords, min_length)
    )
    total = len(tokens)
    rows = [
        (kw, c, round(100 * c / total, 2))
        for kw, c in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    ]
    if top_k:
        rows = rows[:top_k]
    return pd.DataFrame(rows, columns=columns)


def target_keyword_report(text: str, keyword: str) -> dict[str, object]:
    """Count a phrase and rate its density (1-2 % is a common SEO sweet spot)."""
    tokens = tokenize(text)
    target = tokenize(keyword)
    if not tokens or not target:
        return {"count": 0, "density": 0.0, "verdict": "Enter text and a keyword."}
    count = sum(1 for g in ngrams(tokens, len(target)) if list(g) == target)
    density = round(100 * count * len(target) / len(tokens), 2)
    if count == 0:
        verdict = "Not found: consider using the keyword in the text."
    elif density < 0.5:
        verdict = "Low: the keyword could appear a little more often."
    elif density <= 2.5:
        verdict = "Good: natural keyword usage."
    else:
        verdict = "High: risk of keyword stuffing; use synonyms."
    return {"count": count, "density": density, "verdict": verdict}


def text_from_url(url: str, timeout: float = 15.0) -> str:
    """Fetch a web page and return its visible text."""
    if not re.match(r"^https?://", url.strip(), re.IGNORECASE):
        url = "https://" + url.strip()
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    for tag in soup(["script", "style", "noscript", "nav", "footer", "header"]):
        tag.decompose()
    return re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
