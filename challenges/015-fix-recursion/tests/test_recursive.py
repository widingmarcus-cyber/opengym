"""Tests for Challenge 015: Fix the Recursion Bugs."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from recursive import factorial, fibonacci, flatten, sum_nested


# --- Factorial ---

def test_factorial_zero():
    assert factorial(0) == 1


def test_factorial_one():
    assert factorial(1) == 1


def test_factorial_five():
    assert factorial(5) == 120


# --- Fibonacci ---

def test_fibonacci_zero():
    assert fibonacci(0) == 0


def test_fibonacci_one():
    assert fibonacci(1) == 1


def test_fibonacci_ten():
    assert fibonacci(10) == 55


# --- Flatten ---

def test_flatten_nested():
    assert flatten([1, [2, [3, [4]]]]) == [1, 2, 3, 4]


def test_flatten_empty():
    assert flatten([]) == []
    assert flatten([[], [[]]]) == []


# --- Sum nested ---

def test_sum_nested_flat():
    assert sum_nested([1, 2, 3]) == 6


def test_sum_nested_deep():
    assert sum_nested([1, [2, [3, [4]]]]) == 10
    assert sum_nested([]) == 0
