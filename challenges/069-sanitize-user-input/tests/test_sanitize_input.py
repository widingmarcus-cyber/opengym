"""Tests for Challenge 069: Sanitize User Input."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from renderer import render_template


def test_basic_rendering():
    result = render_template("Hello {name}!", {"name": "Alice"})
    assert result == "Hello Alice!"


def test_multiple_placeholders():
    result = render_template(
        "Hi {name}, your balance is {balance}.",
        {"name": "Bob", "balance": 100}
    )
    assert result == "Hi Bob, your balance is 100."


def test_empty_user_data_no_placeholders():
    result = render_template("No placeholders here.", {})
    assert result == "No placeholders here."


def test_numeric_value():
    result = render_template("Count: {count}", {"count": 42})
    assert result == "Count: 42"


def test_injection_attribute_access_blocked():
    """Template must not allow attribute access (e.g., {name.__class__})."""
    try:
        result = render_template("Hello {name.__class__.__name__}!", {"name": "Alice"})
        # If no exception, the result must NOT contain the exposed type name
        assert "str" not in result, (
            f"Attribute access leaked type info: got '{result}'. "
            "render_template must block {key.__attr__} patterns."
        )
    except (AttributeError, ValueError, KeyError, TypeError):
        pass  # Raising an exception is an acceptable way to block this


def test_injection_globals_blocked():
    """Template must not allow access to __globals__."""
    try:
        result = render_template("Hello {name.__init__.__globals__}!", {"name": "Alice"})
        assert "__globals__" not in result and "builtins" not in result, \
            "Must not expose __globals__ through format strings"
    except (AttributeError, ValueError, KeyError, TypeError):
        pass  # Raising an exception is acceptable


def test_injection_via_user_data_values():
    """User data values containing format patterns must not be re-interpreted.

    If user submits name="{balance.__class__}", it should render as the
    literal string, not trigger a second round of format resolution.
    """
    result = render_template(
        "Hello {name}!",
        {"name": "{balance.__class__}", "balance": 9999}
    )
    # The literal string "{balance.__class__}" should appear, OR be safely escaped
    # It must NOT resolve to the class of balance (e.g., "<class 'int'>")
    assert "int" not in result and "class" not in result.lower(), (
        f"User data value was re-interpreted as a format string: got '{result}'. "
        "Values like '{{balance.__class__}}' must be treated as literal text."
    )


def test_injection_format_spec_width():
    """Format spec injection must not allow arbitrary output padding."""
    try:
        result = render_template(
            "Value: {name!s:{padding}}",
            {"name": "test", "padding": "100"}
        )
        # If the vulnerable code succeeds, the result will be ~107 chars (padded)
        assert len(result) < 20, (
            f"Format spec injection allowed padding: result is {len(result)} chars. "
            "render_template must not allow user-controlled format specs."
        )
    except (ValueError, KeyError, TypeError):
        pass  # Raising an exception is acceptable


def test_injection_nested_key_access():
    """Template must not allow dict-style subscript access."""
    try:
        result = render_template(
            "Data: {data[secret]}",
            {"data": {"secret": "TOP_SECRET", "public": "ok"}}
        )
        assert "TOP_SECRET" not in result, (
            f"Subscript access leaked data: got '{result}'. "
            "render_template must block {{key[subscript]}} patterns."
        )
    except (KeyError, ValueError, TypeError, IndexError):
        pass  # Raising an exception is acceptable


def test_missing_key_handled():
    """Template referencing a key not in user_data should not crash."""
    try:
        result = render_template("Hello {missing}!", {"name": "Alice"})
        # Either returns with placeholder intact, or raises a controlled error
        assert isinstance(result, str)
    except (KeyError, ValueError, TypeError):
        pass  # Acceptable to raise on missing keys


def test_injection_double_braces_not_format():
    """User data containing {other_key} must not trigger second-pass formatting."""
    result = render_template(
        "Your note: {note}",
        {"note": "{secret}", "secret": "LEAKED"}
    )
    assert "LEAKED" not in result, (
        f"Value was re-interpreted as format string, exposing 'secret': got '{result}'"
    )


def test_injection_class_via_int():
    """Integer value's __class__ must not be accessible via template."""
    try:
        result = render_template("Type: {val.__class__}", {"val": 42})
        assert "int" not in result, (
            f"Attribute access exposed type info: got '{result}'"
        )
    except (AttributeError, ValueError, KeyError, TypeError):
        pass


def test_injection_format_spec_fill():
    """Format spec injection with fill character must be blocked."""
    try:
        result = render_template(
            "X{name:>{width}}X",
            {"name": "hi", "width": "50"}
        )
        assert len(result) < 20, (
            f"Format spec injection allowed padding: result is {len(result)} chars"
        )
    except (ValueError, KeyError, TypeError):
        pass


def test_injection_subclass_access():
    """Template must not allow __subclasses__ access."""
    try:
        result = render_template(
            "Type: {name.__class__.__subclasses__}",
            {"name": "test"}
        )
        # Must not expose subclass list
        assert "subclass" not in result.lower() and "[" not in result, (
            f"Subclass access leaked info: got '{result}'"
        )
    except (AttributeError, ValueError, KeyError, TypeError):
        pass  # Raising is acceptable


def test_injection_mro_access():
    """Template must not allow MRO (method resolution order) access."""
    try:
        result = render_template(
            "MRO: {name.__class__.__mro__}",
            {"name": "test"}
        )
        assert "object" not in result and "str" not in result, (
            f"MRO access leaked type info: got '{result}'"
        )
    except (AttributeError, ValueError, KeyError, TypeError):
        pass  # Raising is acceptable
