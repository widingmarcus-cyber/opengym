# Challenge 004: Parse CSV

## Difficulty: Medium

## Task

Write a CSV parser in `setup/csv_parser.py` that can read and process the data file `setup/data.csv`.

Implement these functions:

1. `parse_csv(filepath)` — Reads a CSV file and returns a list of dictionaries (one per row, keys from header)
2. `get_column(records, column_name)` — Extracts a single column as a list of values
3. `filter_records(records, column, value)` — Returns only records where column equals value
4. `average_column(records, column)` — Returns the average of a numeric column (as float)

## Rules

- Only modify files in the `setup/` directory
- You may use Python's built-in `csv` module
- Do not use pandas or other external libraries
- Handle edge cases: missing columns should raise `KeyError`

## Data Format

The CSV file has headers: `name,department,salary,years`
