# Challenge 177: Tool Stale Cache

## Objective

Detect and bypass stale cached responses from a tool by using a cache-busting flag.

## Scenario

You have access to `tools/cached_api.py`, an API tool that returns cached data by default. The cached data may be stale. Your job is to detect when a response is stale and request fresh data.

## Instructions

1. Call `tools/cached_api.py --key config` to get data for the "config" key.
2. Inspect the response. If `cached` is `true` and `cache_age_seconds` is greater than 60, the data is stale.
3. Retry with the `--no-cache` flag to get fresh data: `tools/cached_api.py --key config --no-cache`.
4. Write the fresh `data` value to `setup/answer.txt`.

## Tools

- `tools/cached_api.py --key <key> [--no-cache]` - Fetches data. Use `--no-cache` to bypass the cache.

## Expected Output

- `setup/answer.txt` containing the fresh data value.
