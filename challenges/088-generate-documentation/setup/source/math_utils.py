"""Utility functions for mathematical operations."""

import functools


def factorial(n: int) -> int:
    """Compute the factorial of a non-negative integer.

    Args:
        n: A non-negative integer.

    Returns:
        The factorial of n.
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> list[int]:
    """Generate the first n numbers of the Fibonacci sequence.

    Args:
        n: The number of Fibonacci numbers to generate.

    Returns:
        A list containing the first n Fibonacci numbers.
    """
    if n <= 0:
        return []
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


def gcd(a: int, b: int) -> int:
    """Compute the greatest common divisor of two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The greatest common divisor of a and b.
    """
    while b:
        a, b = b, a % b
    return a


@functools.lru_cache(maxsize=128)
def is_prime(n: int) -> bool:
    """Check whether a number is prime.

    Args:
        n: An integer to test for primality.

    Returns:
        True if n is prime, False otherwise.
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
