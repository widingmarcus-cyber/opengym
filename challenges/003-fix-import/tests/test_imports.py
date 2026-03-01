"""Tests for Challenge 003: Fix the Import."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from utils import reverse_string, capitalize_words, clamp, average


def test_reverse_string():
    assert reverse_string("hello") == "olleh"
    assert reverse_string("") == ""
    assert reverse_string("a") == "a"


def test_capitalize_words():
    assert capitalize_words("hello world foo") == "Hello World Foo"
    assert capitalize_words("already Capital") == "Already Capital"


def test_clamp():
    assert clamp(15, 0, 10) == 10
    assert clamp(-5, 0, 10) == 0
    assert clamp(5, 0, 10) == 5


def test_average():
    assert average([1, 2, 3, 4, 5]) == 3.0
    assert average([10]) == 10.0
    assert average([]) == 0
