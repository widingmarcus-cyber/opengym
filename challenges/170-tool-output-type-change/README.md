# Challenge 170: Tool Output Type Change

## Objective

Call the converter tool and handle a type mismatch in the output. The tool returns a string representation of a number. Parse it correctly and write the integer value to `setup/answer.txt`.

## Context

Tools may return values in unexpected types. An API might return `"42"` (string) instead of `42` (integer). A robust agent must handle type coercion correctly — recognizing when a string represents a number and converting it appropriately.

## Tools

- `tools/converter.py` — Converts values between formats. Takes `--input` and `--format` arguments.

## Instructions

1. Call `tools/converter.py --input 42 --format json`.
2. The output field will contain `"42"` (a string, not an integer).
3. Parse this string to get the integer value `42`.
4. Write the value to `setup/answer.txt`.

## Expected Behavior

- `--format json` returns `{"output": "42"}` (string type).
- `--format number` returns `{"output": 42}` (integer type).
- `setup/answer.txt` should contain: `42`
