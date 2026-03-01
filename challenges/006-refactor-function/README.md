# Challenge 006: Refactor the Monster Function

## Difficulty: Medium

## Task

The file `setup/report.py` contains a single massive function `generate_report(data)` that does everything — validation, calculation, formatting, and output.

**Your job:** Refactor it into smaller, well-named functions while keeping the exact same behavior. The `generate_report` function must still exist and work as the main entry point.

## Requirements

After refactoring, `setup/report.py` must have:

1. `validate_records(data)` — Validates input data, returns list of valid records. Each record must have `name` (str), `hours` (number >= 0), and `rate` (number > 0).
2. `calculate_pay(hours, rate)` — Calculates pay for a single employee. Overtime (>40 hours) is paid at 1.5x rate.
3. `format_currency(amount)` — Formats a number as `"$X,XXX.XX"` (2 decimal places, comma-separated thousands)
4. `generate_report(data)` — Orchestrates everything. Returns a dict with `employees` (list of dicts with name, hours, rate, pay, formatted_pay) and `total` (formatted total string).

## Rules

- Only modify files in the `setup/` directory
- The output of `generate_report` must match the expected format exactly
- Invalid records should be silently skipped
