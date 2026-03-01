# Challenge 185: Tool Malformed Headers

## Objective

Parse valid JSON data from a tool's output that contains non-JSON warning lines mixed in.

## Scenario

You have access to `tools/buggy_api.py`, a tool that outputs warning messages alongside its JSON response. The output contains non-JSON lines that must be ignored to extract the actual data.

## Instructions

1. Call `tools/buggy_api.py` (no arguments needed).
2. The output will contain multiple lines, some of which are warnings and not valid JSON.
3. Parse the output to find the line containing valid JSON.
4. Extract the `data` field from the JSON.
5. Write the data value to `setup/answer.txt`.

## Tools

- `tools/buggy_api.py` - Returns data with warning lines mixed into the output.

## Expected Output

- `setup/answer.txt` containing the extracted data value.
