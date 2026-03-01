# Challenge 174: Tool Timeout

## Objective

Call the hanging tool, detect the timeout, and fall back to the `--fallback` flag to get a result. Write the fallback value to `setup/answer.txt`.

## Context

Some operations hang or take far too long. A robust agent must detect when a tool times out and use an alternative approach — such as a fallback flag, a different endpoint, or cached data — rather than waiting indefinitely.

## Tools

- `tools/hanging.py` — Simulates a tool that times out on first call. Takes optional `--timeout` and `--fallback` flags. Uses state file.

## Instructions

1. Call `tools/hanging.py` (no flags).
2. The first call will return a timeout error after 2 seconds.
3. Detect the timeout from the response.
4. Call `tools/hanging.py --fallback` to get the fallback result.
5. Write the data value to `setup/answer.txt`.

## Expected Behavior

- First call (no flags): Returns `{"status": "timeout", "error": "Operation timed out"}` after 2 seconds.
- Second call with `--fallback`: Returns immediately with `{"status": "ok", "data": "fallback_value"}`.
- `setup/answer.txt` should contain: `fallback_value`
