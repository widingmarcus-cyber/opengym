"""Tests for Challenge 027: Diagnose the Crash."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from diagnosis import (
    get_error_type,
    get_root_cause_file,
    get_root_cause_line,
    get_fix_description,
)


def test_error_type():
    """The error type should be AttributeError."""
    assert get_error_type() == "AttributeError"


def test_root_cause_file():
    """The root cause is in app.py."""
    assert get_root_cause_file() == "app.py"


def test_root_cause_line():
    """The root cause is the return None on line 17 in parse_metadata()."""
    line = get_root_cause_line()
    assert line == 17, f"Expected line 17 (the 'return None' in parse_metadata), got {line}"


def test_fix_description():
    """The fix description must mention raising an exception."""
    desc = get_fix_description()
    assert isinstance(desc, str)
    assert len(desc) > 10, "Description is too short"
    desc_lower = desc.lower()
    assert "raise" in desc_lower, "Description must mention 'raise'"
    assert "exception" in desc_lower, "Description must mention 'exception'"
