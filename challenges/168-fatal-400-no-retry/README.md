# Challenge 168: Fatal 400 No Retry

## Objective

Call the validator tool with the primary input. If it returns a 400 client error, do NOT retry the same input — instead, use the fallback input from the config. Write the successful result to `setup/answer.txt`.

## Context

HTTP 4xx errors are client errors — retrying the same request won't help. A robust agent must distinguish between retryable server errors (5xx) and non-retryable client errors (4xx). On a 400, the correct strategy is to fix the input or use an alternative, not to retry blindly.

## Tools

- `tools/validator.py` — Validates input data. Takes `--input` argument.

## Setup Files

- `setup/task_config.json` — Contains `primary_input` and `fallback_input` values.

## Instructions

1. Read `setup/task_config.json` to get the primary and fallback inputs.
2. Call `tools/validator.py --input <primary_input>`.
3. If the response status is `400`, do NOT retry with the same input. Instead, call with `--input <fallback_input>`.
4. Write the result to `setup/answer.txt`. The answer should be `true`.

## Expected Behavior

- Primary input "bad_data" returns 400.
- Fallback input "good_data" returns 200 with `{"validated": true}`.
- `setup/answer.txt` should contain: `true`
- The tool should be called exactly 2 times (not retried on 400).
