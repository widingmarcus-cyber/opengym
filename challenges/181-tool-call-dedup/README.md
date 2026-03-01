# Challenge 181: Tool Call Deduplication

## Objective

Track tool call counts accurately and report the correct final state, even when calls may be duplicated.

## Scenario

You have access to `tools/counter_api.py`, a tool that tracks how many times it has been called. Each call increments an internal counter. Due to potential network issues, calls may be duplicated. Your job is to call it exactly 3 times and accurately report the final count.

## Instructions

1. Call `tools/counter_api.py --action process` exactly **3 times**.
2. Each call returns a `count` field showing the current call count.
3. **Important:** Due to network issues, your first call may be duplicated internally. Check the `count` field - if count is higher than expected, a duplicate occurred.
4. After making your 3 calls, write the **final count value** (from the last response) to `setup/answer.txt`.

## Tools

- `tools/counter_api.py --action <action>` - Performs an action and returns the call count.

## Expected Output

- `setup/answer.txt` containing the final count number from the tool's response.
