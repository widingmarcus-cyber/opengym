# Challenge 183: Tool Encoding Change

## Objective

Handle text encoding differences from a tool and ensure the output is in the correct encoding.

## Scenario

You have access to `tools/text_api.py`, a tool that returns text content. The tool supports different encodings. A configuration file specifies what encoding is required. Your job is to get the text in the correct encoding.

## Instructions

1. Read `setup/config.json` to find the required encoding.
2. Call `tools/text_api.py` (default encoding is UTF-8).
3. Optionally, call with `--encoding <encoding>` to get text in a specific encoding.
4. Ensure the text you write is properly encoded in UTF-8.
5. Write the `text` value to `setup/answer.txt`.

## Tools

- `tools/text_api.py [--encoding <encoding>]` - Returns text in the specified encoding (default: utf-8).

## Expected Output

- `setup/answer.txt` containing the text value in proper UTF-8 encoding.
