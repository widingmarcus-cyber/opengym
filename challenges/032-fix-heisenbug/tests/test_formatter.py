"""Tests for Challenge 032: Fix the Heisenbug."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from formatter import format_report


def test_basic_report():
    """Basic report with default parameters should work."""
    data = [("Apples", 5), ("Bananas", 12), ("Cherries", 3)]
    result = format_report(data)
    assert isinstance(result, str)
    assert "Apples" in result
    assert "Bananas" in result
    assert "Total items: 3" in result


def test_report_with_title():
    """Report with a title should include it in the header."""
    data = [("Revenue", 50000), ("Costs", 30000)]
    result = format_report(data, title="Financial Summary")
    assert "Financial Summary" in result


def test_report_no_header():
    """Report with include_header=False should skip the header."""
    data = [("X", 1)]
    result = format_report(data, title="Test", include_header=False)
    assert "Test" not in result


def test_report_custom_separator():
    """Report with a custom separator character."""
    data = [("Item", 42)]
    result = format_report(data, separator="=")
    assert "=" * 10 in result


def test_report_empty_data():
    """Report with no data rows should still render."""
    result = format_report([], title="Empty Report")
    assert "Empty Report" in result
    assert "Total items: 0" in result


def test_report_narrow_width():
    """Report with a narrow max_width should still work."""
    data = [("A", 1)]
    result = format_report(data, max_width=20)
    lines = result.split("\n")
    for line in lines:
        assert len(line) <= 20, f"Line exceeds max_width: '{line}' ({len(line)} chars)"


def test_title_longer_than_max_width():
    """When title is longer than max_width, it should not crash."""
    data = [("Item", 1)]
    long_title = "This Is A Very Long Report Title That Exceeds Width"
    result = format_report(data, title=long_title, max_width=20, include_header=True)
    assert isinstance(result, str)
    assert "Item" in result


def test_title_equal_to_max_width():
    """Title exactly equal to max_width should work."""
    data = [("X", 1)]
    title = "A" * 30
    result = format_report(data, title=title, max_width=30, include_header=True)
    assert isinstance(result, str)


def test_very_small_max_width():
    """Very small max_width should be handled gracefully."""
    data = [("Test", 42)]
    result = format_report(data, max_width=5, include_header=True)
    assert isinstance(result, str)


def test_title_with_small_width_and_header():
    """The specific failing combination: title + small max_width + include_header.

    When title is provided AND max_width < len(title) AND include_header is True,
    the function must not crash (this is the heisenbug).
    """
    data = [("Sales", 100), ("Returns", 5)]
    result = format_report(
        data,
        title="Quarterly Report Summary",
        max_width=15,
        separator="*",
        include_header=True,
    )
    assert isinstance(result, str)
    assert len(result) > 0
    assert "Sales" in result or "Sal" in result


def test_title_one_char_longer_than_width():
    """Title exactly 1 character longer than max_width must not crash."""
    data = [("Alpha", 10), ("Beta", 20)]
    # Title is 21 chars, max_width is 20
    title = "A" * 21
    result = format_report(data, title=title, max_width=20, include_header=True)
    assert isinstance(result, str)
    assert len(result) > 0
    assert "Alpha" in result


def test_title_double_the_max_width():
    """Title twice as long as max_width must not crash."""
    data = [("Gamma", 30)]
    # Title is 40 chars, max_width is 20
    title = "B" * 40
    result = format_report(data, title=title, max_width=20, include_header=True)
    assert isinstance(result, str)
    assert len(result) > 0
    assert "Gamma" in result or "Gam" in result


def test_very_long_title_narrow_width():
    """Very long title (100+ chars) with narrow width (10) must not crash."""
    data = [("Delta", 50), ("Epsilon", 60)]
    title = "X" * 120
    result = format_report(data, title=title, max_width=10, include_header=True)
    assert isinstance(result, str)
    assert len(result) > 0


def test_title_exactly_width_plus_two():
    """Title 2 chars longer than max_width must not crash."""
    data = [("A", 1)]
    title = "Z" * 22
    result = format_report(data, title=title, max_width=20, include_header=True)
    assert isinstance(result, str)


def test_title_three_char_width_one():
    """Title 'ABC' with max_width=1 must not crash."""
    data = [("X", 9)]
    title = "ABC"
    result = format_report(data, title=title, max_width=1, include_header=True)
    assert isinstance(result, str)


def test_title_ten_chars_width_ten():
    """Title exactly 10 chars with max_width=10 (the minimum) must not crash."""
    data = [("A", 1)]
    title = "A" * 10
    result = format_report(data, title=title, max_width=10, include_header=True)
    assert isinstance(result, str)
    assert len(result) > 0


def test_title_eleven_chars_width_ten():
    """Title 11 chars with max_width=10 must not crash."""
    data = [("B", 2)]
    title = "K" * 11
    result = format_report(data, title=title, max_width=10, include_header=True)
    assert isinstance(result, str)
    assert len(result) > 0
