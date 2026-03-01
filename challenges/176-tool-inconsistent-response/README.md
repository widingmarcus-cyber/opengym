# Challenge 176: Tool Inconsistent Response

## Objective

Deal with a tool that returns inconsistent results across successive calls for the same input.

## Scenario

You have access to `tools/flaky_calc.py`, a calculator tool that returns slightly different results on successive calls due to internal drift. Your job is to determine the **correct** result by calling it multiple times and taking the **most common (mode)** value.

## Instructions

1. Call `tools/flaky_calc.py` with `--operation square --input 6` at least **3 times**.
2. Observe that the results may differ between calls.
3. Determine the most frequently returned result (the mode).
4. Write that value to `setup/answer.txt` (just the number, no whitespace or newline issues).

## Tools

- `tools/flaky_calc.py --operation <op> --input <number>` - Performs a calculation. May return inconsistent results.

## Expected Output

- `setup/answer.txt` containing the mode result.
