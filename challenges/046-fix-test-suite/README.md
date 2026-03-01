# Challenge 046: Fix Test Suite

## Difficulty: Easy

## Task

The file `setup/math_utils.py` contains correct implementations of several math functions. The file `setup/test_math_utils.py` contains tests for these functions, but every test has the **wrong expected value**.

**Your job:** Fix the expected values in all 6 test assertions so they match what the functions actually return.

## Functions

1. `factorial(n)` — Returns the factorial of n (e.g., factorial(5) = 120)
2. `fibonacci(n)` — Returns the nth Fibonacci number (0-indexed: fib(0)=0, fib(1)=1, fib(2)=1, ...)
3. `gcd(a, b)` — Returns the greatest common divisor of a and b
4. `lcm(a, b)` — Returns the least common multiple of a and b
5. `is_prime(n)` — Returns True if n is prime, False otherwise
6. `prime_factors(n)` — Returns the list of prime factors of n in ascending order

## Rules

- Only modify files in the `setup/` directory
- Only fix the expected values in assertions — do not change what is being tested
- Do not modify `math_utils.py`
