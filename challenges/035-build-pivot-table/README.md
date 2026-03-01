# Challenge 035: Build Pivot Table

## Difficulty: Medium

## Task

Transform flat sales data into a pivot table. The file `setup/sales_data.json` contains a list of sales records, and you must implement pivot functions in `setup/pivot.py`.

## Requirements

Implement these functions in `setup/pivot.py`:

1. `pivot(records, row_field, col_field, value_field, agg="sum")` -- Build a pivot table from a list of dictionaries. Group by `row_field` (rows) and `col_field` (columns), aggregating `value_field` using the specified aggregation. Supported aggregations: `"sum"` (default) and `"count"`. Return a nested dict: `{row_value: {col_value: aggregated_value}}`.

2. `pivot_to_table(pivot_result)` -- Convert a pivot result dict into a list of lists suitable for tabular display. The first row should be headers: `[""]` followed by sorted column names. Subsequent rows should have the row name followed by values in column order. Row names should also be sorted.

## Data Format

Each record in `setup/sales_data.json` is a dictionary with:
- `region`: One of `"North"`, `"South"`, `"East"`, `"West"`
- `category`: One of `"Electronics"`, `"Clothing"`, `"Food"`
- `amount`: A numeric value (float)
- `quarter`: One of `"Q1"`, `"Q2"`, `"Q3"`, `"Q4"`

## Rules

- Only modify files in the `setup/` directory
- Use only Python standard library modules
- Do not use pandas or other external libraries
- Missing combinations in the pivot should have a value of 0 (for sum) or 0 (for count)
