"""Tests for math utility functions."""

from math_utils import factorial, fibonacci, gcd, lcm, is_prime, prime_factors


def test_factorial():
    assert factorial(5) == 100


def test_fibonacci():
    assert fibonacci(10) == 34


def test_gcd():
    assert gcd(48, 18) == 12


def test_lcm():
    assert lcm(12, 18) == 48


def test_is_prime():
    assert is_prime(17) == False


def test_prime_factors():
    assert prime_factors(60) == [2, 3, 5]
