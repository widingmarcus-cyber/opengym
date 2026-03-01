"""Tests for Challenge 002: Hello Function."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from greeter import greet, greet_many, formal_greet


def test_greet_basic():
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"


def test_greet_empty():
    assert greet("") == "Hello, !"


def test_greet_many():
    result = greet_many(["Alice", "Bob", "Charlie"])
    assert result == ["Hello, Alice!", "Hello, Bob!", "Hello, Charlie!"]


def test_greet_many_empty_list():
    assert greet_many([]) == []


def test_formal_greet_default():
    assert formal_greet("Smith") == "Good day, Mr. Smith."


def test_formal_greet_custom_title():
    assert formal_greet("Smith", title="Dr.") == "Good day, Dr. Smith."
    assert formal_greet("Jones", title="Prof.") == "Good day, Prof. Jones."
