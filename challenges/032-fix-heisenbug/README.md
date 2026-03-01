# Challenge 032: Fix the Heisenbug

## Difficulty: Hard

## Task

A report formatting function works fine with most inputs but crashes with a specific combination of optional parameters. The bug is subtle and only manifests under particular conditions.

Your job is to find the failing parameter combination and fix the function so it handles all valid inputs correctly.

## Files

```
setup/
  formatter.py    # The report formatting module
```

## Function Signature

```python
def format_report(data, title=None, max_width=80, separator="-", include_header=True)
```

## What It Should Do

- Format a list of `(label, value)` pairs into a text report
- Optionally include a centered title in a header section
- Use the separator character for divider lines
- Respect the max_width for line lengths
- Handle all valid combinations of parameters without crashing

## The Problem

The function works with most inputs but crashes under a specific condition involving the interaction of multiple optional parameters. Your job is to find and fix it.

## Rules

- Only modify files in the `setup/` directory
- Do not change the function signature
- The function must produce reasonable output for all valid inputs
- When max_width is smaller than the title, the title should be truncated (not crash)
