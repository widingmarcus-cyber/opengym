"""Tests for Challenge 001: Fix the Syntax Error."""

import sys
from pathlib import Path

# Add setup/ to path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from calculator import add, subtract, multiply, divide, power


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    assert subtract(10, 4) == 6
    assert subtract(0, 5) == -5


def test_multiply():
    assert multiply(3, 7) == 21
    assert multiply(0, 100) == 0


def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5


def test_divide_by_zero():
    assert divide(10, 0) is None


def test_power():
    assert power(2, 3) == 8
    assert power(5, 0) == 1
