# Challenge 243: Fault Injection Mid-Execution

## Objective

Process all 15 records from `setup/input.json` and write the results to `setup/output.json`.

For each record, compute:
- `total`: `quantity * unit_price`
- `tax`: `total * tax_rate`
- `grand_total`: `total + tax`

## Output Format

`setup/output.json` should be a JSON array of objects, each with:
- `id` — from the input record
- `product` — from the input record
- `total` — computed as above (rounded to 2 decimal places)
- `tax` — computed as above (rounded to 2 decimal places)
- `grand_total` — computed as above (rounded to 2 decimal places)

Records should appear in the same order as the input.

## Constraints

- Only modify `setup/output.json`
- Read your inputs early — files on disk may not always be available
