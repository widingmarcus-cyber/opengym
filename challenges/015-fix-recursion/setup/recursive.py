"""Recursive utility functions."""


def factorial(n):
    """Return n! (n factorial).

    factorial(0) = 1
    factorial(1) = 1
    factorial(5) = 120
    """
    return n * factorial(n - 1)


def fibonacci(n):
    """Return the nth Fibonacci number.

    fibonacci(0) = 0
    fibonacci(1) = 1
    fibonacci(2) = 1
    fibonacci(10) = 55
    """
    return fibonacci(n - 1) + fibonacci(n - 2)


def flatten(nested):
    """Recursively flatten a nested list.

    flatten([1, [2, [3]], 4]) = [1, 2, 3, 4]
    flatten([]) = []
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.extend(flatten(item))
    return result


def sum_nested(data):
    """Recursively sum all numbers in a nested list structure.

    sum_nested([1, [2, [3]]]) = 6
    sum_nested([]) = 0
    """
    total = 0
    for item in data:
        total += sum_nested(item)
    return total
