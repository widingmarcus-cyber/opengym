# Challenge 169: Tool Schema Drift

## Objective

Call the data API tool and extract a value even though the response schema has changed from v1 to v2 format. Write the value to `setup/answer.txt`.

## Context

APIs evolve over time. A v1 response might return `{"result": 42}` while v2 returns `{"data": {"value": 42}}`. A robust agent must handle schema changes gracefully — checking for the expected key, and if missing, exploring the response structure to find the data.

## Tools

- `tools/data_api.py` — Data API with versioned responses. Takes `--version` argument (v1, v2).

## Setup Files

- `setup/config.json` — Contains `expected_version: "v1"`, but the tool now defaults to v2.

## Instructions

1. Read `setup/config.json` to understand the expected version.
2. Call `tools/data_api.py` (default, no version arg) to get the data.
3. The response will be in v2 format: `{"data": {"value": 42}}`.
4. Handle the schema difference — the value is at `data.value` instead of `result`.
5. Write the numeric value to `setup/answer.txt`.

## Expected Behavior

- Default call returns v2 format: `{"data": {"value": 42}}`
- `setup/answer.txt` should contain: `42`
