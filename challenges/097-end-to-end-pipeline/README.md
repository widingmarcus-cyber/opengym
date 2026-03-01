# Challenge 097: End to End Pipeline

## Difficulty: Medium

## Task

The file `setup/pipeline.py` contains stubs. Implement a 4-stage data processing pipeline that ingests raw CSV data, validates it, transforms it, and produces a summary report.

## Setup

- `setup/raw_data/users.csv` -- User data (some rows have missing/invalid data).
- `setup/raw_data/transactions.csv` -- Transaction data (some rows have invalid amounts or dates).
- `setup/raw_data/products.csv` -- Product data (some rows have duplicate IDs).
- `setup/pipeline.py` -- Stubs for the 4 pipeline functions.

## Requirements

### Stage 1: Ingest

`ingest(raw_dir) -> dict` -- Read all CSV files from `raw_dir`. Return a dict mapping filename stems to lists of dicts (each dict is one row). For example: `{"users": [{"id": "1", "name": "Alice", ...}, ...]}`.

### Stage 2: Validate

`validate(data) -> tuple[dict, list]` -- Validate the ingested data. Return `(clean_data, errors)` where:
- `clean_data` has the same structure as input but with invalid rows removed.
- `errors` is a list of dicts: `{"source": "users", "row": <row_dict>, "reason": "..."}`.

Validation rules:
- **users**: Must have non-empty `id`, `name`, and `email`. Email must contain `@`.
- **transactions**: Must have non-empty `id`, `user_id`, `product_id`, and `amount`. Amount must be a positive number.
- **products**: Must have non-empty `id`, `name`, and `price`. Price must be a positive number. Remove duplicate IDs (keep first occurrence).

### Stage 3: Transform

`transform(clean_data) -> dict` -- Produce derived data:
- `"user_spending"`: list of dicts `{"user_id": ..., "total": ...}` with total spending per user.
- `"product_revenue"`: list of dicts `{"product_id": ..., "revenue": ...}` with total revenue per product.

### Stage 4: Report

`report(transformed) -> dict` -- Produce summary statistics:
- `"total_revenue"` (float): Sum of all transaction amounts.
- `"active_users"` (int): Number of unique users who made transactions.
- `"top_products"` (list): Top 3 products by revenue as list of `{"product_id": ..., "revenue": ...}`.

## Rules

- Only modify files in the `setup/` directory.
- Use only the Python standard library (csv module is fine).
