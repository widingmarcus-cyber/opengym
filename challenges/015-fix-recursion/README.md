# Challenge 015: Fix the Recursion Bugs

## Difficulty: Easy

## Task

The file `setup/recursive.py` contains four recursive functions. Each one has a broken or missing base case that causes infinite recursion (leading to a `RecursionError`).

**Your job:** Fix the base cases so each function terminates correctly.

## Functions

1. `factorial(n)` -- Returns n! (factorial of n). For n=0 or n=1, returns 1.
2. `fibonacci(n)` -- Returns the nth Fibonacci number. fib(0)=0, fib(1)=1.
3. `flatten(nested)` -- Recursively flattens a nested list into a flat list.
4. `sum_nested(data)` -- Recursively sums all numbers in a nested structure (lists within lists).

## Rules

- Only modify files in the `setup/` directory
- Do not change function signatures
- Functions must remain recursive (do not rewrite as iterative)
