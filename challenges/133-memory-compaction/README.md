# Challenge 133: Memory Compaction

**Difficulty:** Hard
**Category:** memory-state
**Dimension:** memory
**Type:** Multi-session (3 steps)

## Objective

Demonstrate that your agent can ingest a large volume of key-value data into persistent memory, selectively compact it by discarding irrelevant entries, and report the final state accurately.

## What This Tests

- Ability to parse and store large datasets into structured persistent memory
- Selective filtering/compaction of memory contents based on a rule
- Accurate counting and reporting of compacted state

## Sessions

1. **Ingest Raw Data** -- Parse `setup/raw_data.txt` (1000 key-value lines) and store ALL entries in `setup/memory.json` as a JSON object.
2. **Compact Memory** -- Compact memory by keeping only keys whose numeric suffix is a multiple of 100 (i.e., key_100, key_200, ..., key_1000). Remove all other entries from `setup/memory.json`.
3. **Report Result** -- Count the number of keys remaining in `setup/memory.json` and write that count to `setup/answer.txt`.

## Constraints

- `setup/memory.json` must contain exactly 10 keys after compaction.
- The 10 keys must be: key_100, key_200, key_300, key_400, key_500, key_600, key_700, key_800, key_900, key_1000.
- `setup/answer.txt` must contain exactly the string "10".
