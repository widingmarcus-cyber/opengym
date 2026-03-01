"""Tests for Challenge 012: Fix the Encoding Bug."""

import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from text_processor import read_file, count_characters, reverse_text, extract_words, truncate


def test_read_file_with_unicode():
    """read_file should handle files with emoji and accented characters."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("Caf\u00e9 \u2615 hello \U0001f600")
        path = f.name
    try:
        content = read_file(path)
        assert "Caf\u00e9" in content
        assert "\u2615" in content
        assert "\U0001f600" in content
    finally:
        os.unlink(path)


def test_read_sample_file():
    """read_file should successfully read the provided sample.txt."""
    sample_path = str(Path(__file__).parent.parent / "setup" / "sample.txt")
    content = read_file(sample_path)
    assert "Caf\u00e9" in content
    assert len(content) > 0


def test_count_characters():
    """count_characters should count Unicode characters, not bytes."""
    assert count_characters("hello") == 5
    assert count_characters("Caf\u00e9") == 4
    assert count_characters("\U0001f600\U0001f600\U0001f600") == 3
    assert count_characters("") == 0


def test_reverse_text_unicode():
    """reverse_text should correctly reverse strings with multi-byte characters."""
    assert reverse_text("hello") == "olleh"
    assert reverse_text("Caf\u00e9") == "\u00e9faC"
    assert reverse_text("\U0001f600abc") == "cba\U0001f600"


def test_extract_words_unicode():
    """extract_words should handle punctuation around Unicode words."""
    result = extract_words("Caf\u00e9, \u00fcber, na\u00efve!")
    assert "Caf\u00e9" in result
    assert "\u00fcber" in result
    assert "na\u00efve" in result


def test_truncate_by_characters():
    """truncate should count characters, not bytes, for the limit."""
    assert truncate("hello", 10) == "hello"
    assert truncate("hello world", 5) == "hello..."
    assert truncate("Caf\u00e9 latte", 4) == "Caf\u00e9..."
    assert truncate("\U0001f600\U0001f600\U0001f600", 2) == "\U0001f600\U0001f600..."
