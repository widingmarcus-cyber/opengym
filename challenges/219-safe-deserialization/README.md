# Challenge 219: Safe Deserialization

## Objective

Replace **unsafe deserialization** methods (`pickle.loads`, `eval`) with safe alternatives (`json.loads`, `ast.literal_eval`) in a data processing module.

## Setup

- `setup/loader.py` — A module with three functions that deserialize data from different sources:
  - `load_config(data_bytes)` — Loads configuration from bytes using `pickle.loads` (unsafe).
  - `parse_user_input(input_string)` — Parses user-provided data using `eval` (unsafe).
  - `load_message(json_string)` — Already uses `json.loads` (safe — do NOT change this).

## What You Must Do

1. Replace `pickle.loads` in `load_config` with `json.loads` (data will be JSON-encoded bytes).
2. Replace `eval` in `parse_user_input` with `ast.literal_eval` for safe parsing of Python literals.
3. Do NOT change `load_message` — it is already safe.
4. Ensure all three functions still work for legitimate inputs:
   - `load_config(b'{"key": "value"}')` returns `{"key": "value"}`
   - `parse_user_input("{'name': 'Alice', 'age': 30}")` returns `{'name': 'Alice', 'age': 30}`
   - `load_message('{"msg": "hello"}')` returns `{"msg": "hello"}`

## Constraints

- Do NOT change function signatures.
- `load_config` must use `json.loads`, not `pickle`.
- `parse_user_input` must use `ast.literal_eval`, not `eval`.
- Both functions must return `{"status": "ok", "data": ...}` on success and `{"status": "error", "message": "..."}` on failure.
