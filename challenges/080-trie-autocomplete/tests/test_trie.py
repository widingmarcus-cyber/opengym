"""Tests for Challenge 080: Trie Autocomplete."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from trie import Trie


def test_insert_and_search():
    t = Trie()
    t.insert("hello")
    assert t.search("hello") is True
    assert t.search("hell") is False


def test_search_empty_trie():
    t = Trie()
    assert t.search("anything") is False


def test_starts_with():
    t = Trie()
    t.insert("hello")
    assert t.starts_with("hel") is True
    assert t.starts_with("hello") is True
    assert t.starts_with("help") is False


def test_autocomplete_by_frequency():
    t = Trie()
    t.insert("apple", 5)
    t.insert("app", 3)
    t.insert("application", 2)
    result = t.autocomplete("app")
    assert result == ["apple", "app", "application"]


def test_autocomplete_alphabetical_tiebreak():
    t = Trie()
    t.insert("cat", 2)
    t.insert("car", 2)
    t.insert("cap", 2)
    result = t.autocomplete("ca")
    assert result == ["cap", "car", "cat"]


def test_autocomplete_limit_k():
    t = Trie()
    t.insert("a", 1)
    t.insert("ab", 2)
    t.insert("abc", 3)
    t.insert("abcd", 4)
    result = t.autocomplete("a", k=2)
    assert result == ["abcd", "abc"]


def test_autocomplete_no_matches():
    t = Trie()
    t.insert("hello")
    result = t.autocomplete("xyz")
    assert result == []


def test_autocomplete_empty_prefix():
    t = Trie()
    t.insert("banana", 3)
    t.insert("apple", 5)
    result = t.autocomplete("", k=2)
    assert result == ["apple", "banana"]


def test_delete_existing():
    t = Trie()
    t.insert("apple")
    assert t.delete("apple") is True
    assert t.search("apple") is False


def test_delete_nonexistent():
    t = Trie()
    t.insert("apple")
    assert t.delete("app") is False


def test_delete_preserves_other_words():
    t = Trie()
    t.insert("apple", 5)
    t.insert("app", 3)
    t.delete("app")
    assert t.search("app") is False
    assert t.search("apple") is True
    assert t.starts_with("app") is True


def test_insert_adds_frequency():
    t = Trie()
    t.insert("hello", 3)
    t.insert("hello", 2)
    t.insert("world", 4)
    result = t.autocomplete("", k=2)
    assert result == ["hello", "world"]
