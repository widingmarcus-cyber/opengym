# Challenge 178: Tool Large Payload

## Objective

Handle paginated data from a tool by fetching all available pages and computing the sum of all values. Write the total to `setup/answer.txt`.

## Scenario

You have access to a data dump tool that returns records in pages. You need to fetch all pages until no more data remains, then compute an aggregate.

## Instructions

1. Call the data dump tool starting at page 1.
2. Inspect the response to find pagination metadata (e.g., whether more pages exist).
3. Continue fetching subsequent pages until all data has been retrieved.
4. Sum all `value` fields from all records across all pages.
5. Write the total sum to `setup/answer.txt`.

## Tools

- `tools/data_dump.py --page <N>` — Returns page N of records. Run with `--help` for details.

## Notes

- Do not assume a fixed number of pages — use the response metadata.
- The sum must be computed from the actual tool responses.
