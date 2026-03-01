# Challenge 174: Tool Timeout

## Objective

Call a tool that may hang or timeout. Find an alternative way to get a successful response. Write the result to `setup/answer.txt`.

## Context

Some operations hang or take far too long. A robust agent must detect when a tool is unresponsive and explore alternative approaches — such as different flags, fallback modes, or cached data — rather than waiting indefinitely or giving up.

## Tools

- `tools/hanging.py` — A tool that may hang or timeout. Run with `--help` to discover available flags and modes.

## Instructions

1. Call the tool and observe its behavior.
2. If it hangs or returns a timeout/error, explore the tool's help to find alternative invocation options.
3. Use the appropriate approach to get a successful response.
4. Extract the data value from the successful response.
5. Write it to `setup/answer.txt`.

## Notes

- Read the tool's `--help` output carefully.
- The tool must be called at least twice (experience the problem, then solve it).
