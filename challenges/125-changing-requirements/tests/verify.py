#!/usr/bin/env python3
"""Verify Challenge 125: Changing Requirements — converter handles C, F, K and unified convert()."""

import json
import math
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

sys.path.insert(0, SETUP_DIR)

results = []


def check(name, passed, message=""):
    results.append({"test": name, "passed": passed, "message": message})


def approx(a, b, tol=0.01):
    """Check if two numbers are approximately equal."""
    if a is None or b is None:
        return False
    return abs(float(a) - float(b)) < tol


def main():
    try:
        import converter

        # Test 1: celsius_to_fahrenheit(100) == 212
        try:
            result = converter.celsius_to_fahrenheit(100)
            check(
                "c_to_f_100",
                approx(result, 212),
                f"celsius_to_fahrenheit(100) = {result}, expected 212",
            )
        except Exception as e:
            check("c_to_f_100", False, f"Error: {e}")

        # Test 2: fahrenheit_to_celsius(32) == 0
        try:
            result = converter.fahrenheit_to_celsius(32)
            check(
                "f_to_c_32",
                approx(result, 0),
                f"fahrenheit_to_celsius(32) = {result}, expected 0",
            )
        except Exception as e:
            check("f_to_c_32", False, f"Error: {e}")

        # Test 3: celsius_to_kelvin(0) == 273.15
        try:
            result = converter.celsius_to_kelvin(0)
            check(
                "c_to_k_0",
                approx(result, 273.15),
                f"celsius_to_kelvin(0) = {result}, expected 273.15",
            )
        except Exception as e:
            check("c_to_k_0", False, f"Error: {e}")

        # Test 4: kelvin_to_celsius(373.15) == 100
        try:
            result = converter.kelvin_to_celsius(373.15)
            check(
                "k_to_c_373",
                approx(result, 100),
                f"kelvin_to_celsius(373.15) = {result}, expected 100",
            )
        except Exception as e:
            check("k_to_c_373", False, f"Error: {e}")

        # Test 5: convert(100, "C", "F") == 212
        try:
            result = converter.convert(100, "C", "F")
            check(
                "convert_c_to_f",
                approx(result, 212),
                f"convert(100, 'C', 'F') = {result}, expected 212",
            )
        except Exception as e:
            check("convert_c_to_f", False, f"Error: {e}")

        # Test 6: convert(100, "C", "K") == 373.15
        try:
            result = converter.convert(100, "C", "K")
            check(
                "convert_c_to_k",
                approx(result, 373.15),
                f"convert(100, 'C', 'K') = {result}, expected 373.15",
            )
        except Exception as e:
            check("convert_c_to_k", False, f"Error: {e}")

        # Test 7: convert(212, "F", "C") == 100
        try:
            result = converter.convert(212, "F", "C")
            check(
                "convert_f_to_c",
                approx(result, 100),
                f"convert(212, 'F', 'C') = {result}, expected 100",
            )
        except Exception as e:
            check("convert_f_to_c", False, f"Error: {e}")

        # Test 8: convert(212, "F", "K") == 373.15
        try:
            result = converter.convert(212, "F", "K")
            check(
                "convert_f_to_k",
                approx(result, 373.15),
                f"convert(212, 'F', 'K') = {result}, expected 373.15",
            )
        except Exception as e:
            check("convert_f_to_k", False, f"Error: {e}")

        # Test 9: convert raises ValueError for unknown units
        try:
            converter.convert(100, "C", "X")
            check("convert_unknown_unit", False, "Expected ValueError for unknown unit 'X'")
        except ValueError:
            check("convert_unknown_unit", True, "ValueError raised for unknown unit")
        except Exception as e:
            check("convert_unknown_unit", False, f"Expected ValueError, got {type(e).__name__}: {e}")

        # Test 10: Original functions still work (regression check)
        try:
            r1 = converter.celsius_to_fahrenheit(0)
            r2 = converter.fahrenheit_to_celsius(212)
            ok = approx(r1, 32) and approx(r2, 100)
            check(
                "original_functions_still_work",
                ok,
                f"c_to_f(0)={r1} (exp 32), f_to_c(212)={r2} (exp 100)",
            )
        except Exception as e:
            check("original_functions_still_work", False, f"Error: {e}")

    except ImportError as e:
        for name in [
            "c_to_f_100", "f_to_c_32", "c_to_k_0", "k_to_c_373",
            "convert_c_to_f", "convert_c_to_k", "convert_f_to_c",
            "convert_f_to_k", "convert_unknown_unit", "original_functions_still_work",
        ]:
            check(name, False, f"Could not import converter: {e}")

    print_results()


def print_results():
    for r in results:
        print(json.dumps(r))


if __name__ == "__main__":
    main()
