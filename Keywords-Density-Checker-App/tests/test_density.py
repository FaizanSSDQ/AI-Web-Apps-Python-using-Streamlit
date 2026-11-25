"""Tests for the keyword density engine."""

from density import keyword_density, target_keyword_report, text_stats, tokenize

TEXT = (
    "Embedded systems are everywhere. Embedded systems run firmware! "
    "Good firmware makes embedded systems reliable."
)


def test_tokenize_keeps_contractions_and_hyphens():
    assert tokenize("It's a low-power MCU, isn’t it?") == [
        "it's",
        "a",
        "low-power",
        "mcu",
        "isn't",
        "it",
    ]


def test_text_stats():
    stats = text_stats(TEXT)
    assert stats["words"] == 14
    assert stats["sentences"] == 3
    assert stats["avg_words_per_sentence"] == 4.7


def test_unigram_density_ignores_stopwords():
    table = keyword_density(TEXT, n=1, min_length=3)
    top = table.iloc[0]
    assert {top["keyword"], table.iloc[1]["keyword"]} == {"embedded", "systems"}
    assert top["count"] == 3
    assert top["density_%"] == 21.43  # 3 of 14 words
    assert "are" not in set(table["keyword"])


def test_bigram_density():
    table = keyword_density(TEXT, n=2)
    assert table.iloc[0]["keyword"] == "embedded systems"
    assert table.iloc[0]["count"] == 3


def test_stopwords_can_be_kept():
    table = keyword_density(TEXT, n=1, remove_stopwords=False, min_length=1)
    assert "are" in set(table["keyword"])


def test_empty_text():
    assert keyword_density("").empty
    assert text_stats("")["words"] == 0


def test_target_keyword_report():
    report = target_keyword_report(TEXT, "Embedded Systems")
    assert report["count"] == 3
    assert report["density"] == 42.86  # 3 x 2 words of 14
    assert report["verdict"].startswith("High")
    assert target_keyword_report(TEXT, "bluetooth")["count"] == 0
