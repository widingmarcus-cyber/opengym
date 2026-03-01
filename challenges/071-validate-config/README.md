# Challenge 071: Validate Config

## Difficulty: Medium

## Task

The file `setup/config_loader.py` contains a `load_config` function that accepts a configuration dictionary and returns a config object. Currently it accepts any values without validation, including dangerous or invalid inputs.

Add proper validation to reject invalid configurations.

## Setup

- `setup/config_loader.py` — Contains the `load_config` function that needs validation

## Requirements

Add validation to `load_config(data)` so that:

1. Valid configurations are accepted and returned as-is (as a dict or SimpleNamespace)
2. Port numbers must be between 1 and 65535 (reject 0, negative, or > 65535)
3. File paths must not contain path traversal sequences (`..`)
4. Database name must not be empty or whitespace-only
5. Host must be a non-empty string
6. Invalid configurations raise a `ValueError` with a descriptive message
7. The function validates all fields: `host`, `port`, `database`, `data_dir`

## Rules

- Only modify `setup/config_loader.py`
- The function signature must remain `load_config(data)`
- Raise `ValueError` for all validation failures
