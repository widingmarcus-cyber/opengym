# Challenge 171: Tool Partial JSON

## Objective

Call the streamer tool and handle any incomplete or truncated JSON output. Once you have valid JSON, compute the sum of the data array and write it to `setup/answer.txt`.

## Context

Network issues, buffer limits, or streaming APIs can produce truncated JSON. A robust agent must detect invalid JSON, recognize it as incomplete data, and retry rather than attempting to parse broken output or giving up entirely.

## Tools

- `tools/streamer.py` — Simulates a streaming API. Run with `--help` for options. Uses persistent state.

## Instructions

1. Call the streamer tool.
2. Attempt to parse the output as JSON.
3. If parsing fails (the output may be truncated), call the tool again.
4. Once you receive valid JSON, find the data array in the response.
5. Compute the sum of the array values from the actual response.
6. Write the sum to `setup/answer.txt`.

## Notes

- The tool may not return valid JSON on every call.
- Do not hardcode the answer — compute the sum from the actual response data.
