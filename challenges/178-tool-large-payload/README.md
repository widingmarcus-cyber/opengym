# Challenge 178: Tool Large Payload

## Objective

Handle paginated data from a tool by fetching all pages and aggregating the results.

## Scenario

You have access to `tools/data_dump.py`, a tool that returns data in pages of 50 records each. You need to fetch all pages until no more data is available, then compute an aggregate.

## Instructions

1. Call `tools/data_dump.py --page 1` to get the first page of records.
2. Check the `has_more` field in the response. If `true`, fetch the next page.
3. Continue until `has_more` is `false` or `data` is empty.
4. Each record has an `id` and a `value` field (value = id * 2).
5. Compute the **sum of all `value` fields** across all records.
6. Write the sum to `setup/answer.txt`.

## Tools

- `tools/data_dump.py --page <N>` - Returns page N of records (50 per page).

## Expected Output

- `setup/answer.txt` containing the total sum of all values.
