# Challenge 171: Tool Partial JSON

## Objective

Call the streamer tool and handle partial/truncated JSON output. If the output is not valid JSON, call the tool again to get the complete response. Write the sum of the data array to `setup/answer.txt`.

## Context

Network issues, buffer limits, or streaming APIs can produce truncated JSON. A robust agent must detect invalid JSON, recognize it as incomplete data, and retry rather than attempting to parse broken output or giving up entirely.

## Tools

- `tools/streamer.py` — Simulates a streaming API that may return partial JSON. Uses state file to track calls.

## Instructions

1. Call `tools/streamer.py`.
2. Attempt to parse the output as JSON.
3. If parsing fails (truncated output), call the tool again.
4. On the second call, you will get complete, valid JSON.
5. Sum the values in the `data` array.
6. Write the sum to `setup/answer.txt`.

## Expected Behavior

- First call returns truncated JSON: `{"data": [1, 2, 3` (invalid).
- Second call returns complete JSON: `{"data": [1, 2, 3, 4, 5], "complete": true}`.
- Sum of `[1, 2, 3, 4, 5]` = 15.
- `setup/answer.txt` should contain: `15`
