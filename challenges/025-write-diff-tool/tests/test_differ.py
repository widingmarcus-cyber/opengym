"""Tests for Challenge 025: Write Diff Tool."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from differ import diff, unified_diff, DiffLine


def test_identical_texts():
    result = diff("hello\nworld", "hello\nworld")
    assert all(d.type == "equal" for d in result)
    assert [d.content for d in result] == ["hello", "world"]


def test_completely_different():
    result = diff("aaa\nbbb", "ccc\nddd")
    removed = [d for d in result if d.type == "removed"]
    added = [d for d in result if d.type == "added"]
    assert [d.content for d in removed] == ["aaa", "bbb"]
    assert [d.content for d in added] == ["ccc", "ddd"]


def test_addition_only():
    result = diff("hello", "hello\nworld")
    types = [d.type for d in result]
    assert "equal" in types
    assert "added" in types
    equal_lines = [d.content for d in result if d.type == "equal"]
    added_lines = [d.content for d in result if d.type == "added"]
    assert "hello" in equal_lines
    assert "world" in added_lines


def test_removal_only():
    result = diff("hello\nworld", "hello")
    types = [d.type for d in result]
    assert "equal" in types
    assert "removed" in types
    removed_lines = [d.content for d in result if d.type == "removed"]
    assert "world" in removed_lines


def test_empty_first_text():
    result = diff("", "hello\nworld")
    assert all(d.type == "added" for d in result)
    assert [d.content for d in result] == ["hello", "world"]


def test_empty_second_text():
    result = diff("hello\nworld", "")
    assert all(d.type == "removed" for d in result)
    assert [d.content for d in result] == ["hello", "world"]


def test_both_empty():
    result = diff("", "")
    assert result == []


def test_unified_diff_format():
    result = unified_diff("hello\nworld", "hello\nearth")
    lines = result.split("\n")
    assert " hello" in lines
    assert "-world" in lines
    assert "+earth" in lines


def test_unified_diff_identical():
    result = unified_diff("hello\nworld", "hello\nworld")
    lines = result.split("\n")
    assert all(line.startswith(" ") for line in lines if line)


def test_mixed_changes():
    a = "line1\nline2\nline3\nline4"
    b = "line1\nmodified\nline3\nnew_line\nline4"
    result = diff(a, b)
    equal_contents = [d.content for d in result if d.type == "equal"]
    assert "line1" in equal_contents
    assert "line3" in equal_contents
    assert "line4" in equal_contents
    removed_contents = [d.content for d in result if d.type == "removed"]
    added_contents = [d.content for d in result if d.type == "added"]
    assert "line2" in removed_contents
    assert "modified" in added_contents
    assert "new_line" in added_contents
