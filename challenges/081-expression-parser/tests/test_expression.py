"""Tests for Challenge 081: Expression Parser."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import pytest
from expression import evaluate


def test_simple_addition():
    assert evaluate("2 + 3") == 5.0


def test_simple_subtraction():
    assert evaluate("10 - 4") == 6.0


def test_multiplication():
    assert evaluate("3 * 7") == 21.0


def test_division():
    assert evaluate("15 / 4") == 3.75


def test_operator_precedence():
    assert evaluate("2 + 3 * 4") == 14.0


def test_parentheses():
    assert evaluate("(2 + 3) * 4") == 20.0


def test_nested_parentheses():
    assert evaluate("((2 + 3) * (4 - 1))") == 15.0


def test_exponentiation():
    assert evaluate("2 ** 10") == 1024.0


def test_exponentiation_right_associative():
    assert evaluate("2 ** 3 ** 2") == 512.0


def test_unary_minus():
    assert evaluate("-3 + 4") == 1.0


def test_unary_minus_in_expression():
    assert evaluate("5 * -2") == -10.0


def test_variables():
    assert evaluate("x + y * 2", {"x": 3, "y": 5}) == 13.0


def test_variable_not_found():
    with pytest.raises(ValueError):
        evaluate("x + 1")


def test_unbalanced_parentheses():
    with pytest.raises(ValueError):
        evaluate("(2 + 3")


def test_invalid_expression():
    with pytest.raises(ValueError):
        evaluate("2 + + 3")


def test_complex_expression():
    result = evaluate("(2 + 3) ** 2 / 5 - 1")
    assert abs(result - 4.0) < 1e-9


def test_whitespace_handling():
    assert evaluate("  2  +  3  ") == 5.0
