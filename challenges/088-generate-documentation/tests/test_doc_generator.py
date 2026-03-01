"""Tests for Challenge 088: Generate Documentation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from doc_generator import generate_docs

SOURCE_DIR = str(Path(__file__).parent.parent / "setup" / "source")


def _get_docs():
    return generate_docs(SOURCE_DIR)


def test_output_is_string():
    result = _get_docs()
    assert isinstance(result, str)
    assert len(result) > 0


def test_contains_module_headings():
    result = _get_docs()
    assert "# Module: data_utils" in result
    assert "# Module: math_utils" in result
    assert "# Module: string_utils" in result


def test_modules_sorted_alphabetically():
    result = _get_docs()
    pos_data = result.index("# Module: data_utils")
    pos_math = result.index("# Module: math_utils")
    pos_string = result.index("# Module: string_utils")
    assert pos_data < pos_math < pos_string


def test_contains_function_names():
    result = _get_docs()
    assert "factorial" in result
    assert "fibonacci" in result
    assert "gcd" in result
    assert "is_prime" in result
    assert "slugify" in result
    assert "truncate" in result
    assert "word_count" in result
    assert "flatten" in result
    assert "chunk" in result
    assert "deep_merge" in result
    assert "validate_schema" in result


def test_contains_function_signatures():
    result = _get_docs()
    assert "n: int" in result
    assert "-> int" in result
    assert "-> bool" in result
    assert "-> str" in result
    assert "text: str" in result


def test_contains_docstrings():
    result = _get_docs()
    assert "Compute the factorial of a non-negative integer" in result
    assert "Convert a string into a URL-friendly slug" in result
    assert "Flatten a nested list into a single-level list" in result
    assert "Deep merge two dictionaries" in result


def test_function_signatures_in_code_blocks():
    result = _get_docs()
    assert "`factorial(n: int) -> int`" in result or "```" in result


def test_contains_return_types():
    result = _get_docs()
    assert "-> bool" in result
    assert "-> str" in result
    assert "-> list[str]" in result or "-> list" in result
