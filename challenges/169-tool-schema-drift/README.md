# Challenge 169: Tool Schema Drift

## Objective

Call the data API tool and extract the numeric value from its response, even if the response format doesn't match what you expect. Write the value to `setup/answer.txt`.

## Context

APIs evolve over time. Response schemas change between versions — keys get renamed, nested structures get added or flattened. A robust agent must not assume a fixed schema. Instead, it should inspect the response, explore its structure, and extract the data regardless of format changes.

## Tools

- `tools/data_api.py` — Data API with versioned responses. Run with `--help` for usage.

## Setup Files

- `setup/config.json` — Contains the expected API version and configuration.

## Instructions

1. Read `setup/config.json` to understand the expected version.
2. Call the data API tool to get the response.
3. Parse the JSON response and locate the numeric value — it may not be where you expect.
4. Handle any schema differences programmatically.
5. Write the extracted numeric value to `setup/answer.txt`.

## Notes

- The tool's actual response format may differ from what the config suggests.
- Do not hardcode assumptions about the JSON structure.
