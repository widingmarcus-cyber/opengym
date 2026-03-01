# Challenge 135: Large Memory Pagination

**Difficulty:** Hard
**Category:** memory-state
**Dimension:** memory
**Type:** Multi-session (2 steps)

## Objective

Demonstrate that your agent can store a large number of facts across multiple paginated memory files (each limited to 50 entries), and then retrieve a specific fact by determining which page contains it.

## What This Tests

- Splitting large datasets into fixed-size pages for persistent storage
- Navigating paginated memory to find a specific entry
- Correct indexing and retrieval from a multi-file memory store

## Sessions

1. **Store 200 Facts** -- Read all 200 facts from the step instructions and store them in `setup/memory/` as paginated JSON files. Each file may contain at most 50 entries. You must create `page_1.json`, `page_2.json`, `page_3.json`, and `page_4.json`.
2. **Retrieve Fact 137** -- Determine which page contains fact 137, read that page, and write the full text of fact 137 to `setup/answer.txt`.

## Constraints

- `setup/memory/` must contain exactly 4 page files.
- Each page file must contain at most 50 entries.
- The total number of entries across all pages must be 200.
- `setup/answer.txt` must contain the exact text: "The speed of light is 299792458 m/s"
