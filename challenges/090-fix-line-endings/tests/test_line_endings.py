"""Tests for Challenge 090: Fix Line Endings."""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from line_endings import normalize_endings, detect_endings, fix_file


def test_normalize_crlf_to_lf():
    text = "hello\r\nworld\r\n"
    assert normalize_endings(text, "\n") == "hello\nworld\n"


def test_normalize_mixed_to_lf():
    text = "line1\r\nline2\nline3\r\nline4\n"
    assert normalize_endings(text, "\n") == "line1\nline2\nline3\nline4\n"


def test_normalize_to_crlf():
    text = "hello\nworld\n"
    assert normalize_endings(text, "\r\n") == "hello\r\nworld\r\n"


def test_normalize_cr_to_lf():
    text = "hello\rworld\r"
    assert normalize_endings(text, "\n") == "hello\nworld\n"


def test_detect_lf():
    assert detect_endings("hello\nworld\n") == "lf"


def test_detect_crlf():
    assert detect_endings("hello\r\nworld\r\n") == "crlf"


def test_detect_mixed():
    assert detect_endings("hello\r\nworld\n") == "mixed"


def test_fix_file_normalizes():
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False) as f:
        f.write(b"line1\r\nline2\nline3\r\nline4\n")
        path = f.name
    try:
        fix_file(path, "\n")
        with open(path, "rb") as f:
            content = f.read()
        assert content == b"line1\nline2\nline3\nline4\n"
    finally:
        os.unlink(path)
