# Challenge 034: Normalize Messy Data

## Difficulty: Easy

## Task

Clean a dataset with inconsistent formatting. The file `setup/messy_data.json` contains a list of records with various formatting issues, and you must implement a normalizer in `setup/normalizer.py`.

## Requirements

Implement this function in `setup/normalizer.py`:

1. `normalize_records(records)` -- Takes a list of dictionaries and returns a new list of normalized dictionaries with the following transformations applied:
   - **Dates**: The `date` field may appear in three formats: `"2024-01-15"` (ISO), `"Jan 15, 2024"` (month name), or `"15/01/2024"` (DD/MM/YYYY). Normalize all dates to ISO format `"YYYY-MM-DD"`.
   - **Status**: The `status` field may have inconsistent casing like `"Active"`, `"ACTIVE"`, `"active"`. Normalize all to lowercase.
   - **Names**: The `name` field may have leading or trailing whitespace. Strip all whitespace.
   - **Duplicates**: Remove exact duplicate records (after normalization, if two records are identical, keep only one).

## Data Format

Each record in the input list is a dictionary with keys: `name`, `date`, `status`, `email`.

## Rules

- Only modify files in the `setup/` directory
- Use only Python standard library modules
- Do not use pandas or other external libraries
- Preserve the original order of records (keep the first occurrence of duplicates)
