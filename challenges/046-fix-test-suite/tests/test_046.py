"""Hidden tests for Challenge 046: Fix Test Suite."""

import sys
import os
import subprocess
import tempfile
import shutil
from pathlib import Path

# Add setup/ to path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

SETUP_DIR = Path(__file__).parent.parent / "setup"


def _run_single_test(test_name):
    """Run a single test from the agent's test file and return whether it passes."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "test_math_utils.py", "-v",
         "-k", test_name, "--tb=short"],
        capture_output=True,
        text=True,
        cwd=str(SETUP_DIR),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return result.returncode == 0


def test_factorial_fixed():
    """The agent should have fixed factorial(5) == 120."""
    assert _run_single_test("test_factorial"), (
        "test_factorial still fails — factorial(5) should equal 120"
    )


def test_fibonacci_fixed():
    """The agent should have fixed fibonacci(10) == 55."""
    assert _run_single_test("test_fibonacci"), (
        "test_fibonacci still fails — fibonacci(10) should equal 55"
    )


def test_gcd_fixed():
    """The agent should have fixed gcd(48, 18) == 6."""
    assert _run_single_test("test_gcd"), (
        "test_gcd still fails — gcd(48, 18) should equal 6"
    )


def test_lcm_fixed():
    """The agent should have fixed lcm(12, 18) == 36."""
    assert _run_single_test("test_lcm"), (
        "test_lcm still fails — lcm(12, 18) should equal 36"
    )


def test_is_prime_fixed():
    """The agent should have fixed is_prime(17) == True."""
    assert _run_single_test("test_is_prime"), (
        "test_is_prime still fails — is_prime(17) should equal True"
    )


def test_prime_factors_fixed():
    """The agent should have fixed prime_factors(60) == [2, 2, 3, 5]."""
    assert _run_single_test("test_prime_factors"), (
        "test_prime_factors still fails — prime_factors(60) should equal [2, 2, 3, 5]"
    )
