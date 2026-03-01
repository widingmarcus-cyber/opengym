# Challenge 126: Resource Constraints

## Difficulty: Hard
## Category: Budget Planning
## Dimension: Planning

## Description

Gather information about 10 items using a lookup tool that has a **limited budget of 5 total calls**. Each call can look up 1 to 3 items at once (comma-separated input). You must plan your calls efficiently to get all 10 items' data within the 5-call budget.

This tests whether an agent can plan resource usage before acting, rather than making one call per item.

## Objective

1. Read the list of items from `setup/items.txt`
2. Use `tools/lookup.py` to look up item data (max 3 items per call, max 5 calls total)
3. Write all results to `setup/results.json`

## Constraints

- The lookup tool tracks usage in `tools/.state/budget.json`
- Maximum 5 total calls to the lookup tool
- Each call accepts 1-3 comma-separated item names
- 10 items / 3 per call = minimum 4 calls needed (you have 5)

## Usage

```bash
python tools/lookup.py "apple,banana,cherry"
```

## Setup

- `setup/items.txt` — list of 10 items to look up
- `tools/lookup.py` — the lookup tool (budget-limited)
- `tools/.state/budget.json` — budget tracker

## Verification

```bash
python tests/verify.py
```

Checks that all 10 items have correct data and the budget was not exceeded.
