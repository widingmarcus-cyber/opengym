# Challenge 173: Tool Latency Spike

## Objective

Call the slow API tool and wait for the response even though it takes a few seconds. Write the first successful response data to `setup/answer.txt`.

## Context

Some API calls take longer than expected due to latency spikes, cold starts, or heavy processing. A robust agent must be patient — waiting for a slow response rather than timing out prematurely and retrying (which would get a different result).

## Tools

- `tools/slow_api.py` — API that has latency on first call. Takes optional `--timeout` argument. Uses state file to track calls.

## Instructions

1. Call `tools/slow_api.py`.
2. The first call will be slow (takes ~3 seconds) but will succeed.
3. Wait for the response. Do NOT give up early.
4. Extract the `data` value from the response.
5. Write it to `setup/answer.txt`.

## Expected Behavior

- First call: 3-second delay, then returns `{"data": "slow_result"}`.
- Second call (if made): Returns immediately with `{"data": "fast_result"}`.
- `setup/answer.txt` should contain: `slow_result` (from the first call, proving the agent waited).
