# Challenge 040: Extract Duplicate Code

## Difficulty: Easy

## Task

The file `setup/handlers.py` contains four handler functions: `handle_user()`, `handle_product()`, `handle_order()`, and `handle_payment()`. Each one repeats the same validation, type-conversion, and formatting logic inline.

**Your job:** Extract the duplicated logic into a shared helper function while keeping all four handler functions working exactly the same way.

## Requirements

After refactoring, `setup/handlers.py` must have:

1. A shared helper function (e.g., `validate_and_format` or `process_record`) that performs the common validation, type conversion, and output formatting.
2. `handle_user(data)` — Processes a user record. Required fields: `name` (str), `age` (int), `email` (str).
3. `handle_product(data)` — Processes a product record. Required fields: `title` (str), `price` (float), `quantity` (int).
4. `handle_order(data)` — Processes an order record. Required fields: `order_id` (str), `amount` (float), `status` (str).
5. `handle_payment(data)` — Processes a payment record. Required fields: `payment_id` (str), `total` (float), `method` (str).

Each handler must still return the same dict structure as before: `{"valid": True/False, "record": {...}, "summary": "..."}`.

## Rules

- Only modify files in the `setup/` directory
- All four original handler functions must continue to exist and produce identical output
- The duplicated validation/conversion/formatting logic must be extracted into a reusable helper
