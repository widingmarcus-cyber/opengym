# Challenge 128: Memory Overwrite vs Append

**Difficulty:** Easy
**Category:** memory-state
**Dimension:** memory
**Type:** Multi-session (3 steps)

## Objective

Demonstrate that your agent can correctly overwrite an existing key in a persistent memory store, rather than appending a duplicate entry. After updating the key across sessions, recall the correct (latest) value.

## What This Tests

- Correct key-value overwrite semantics in persistent storage
- Avoiding duplicate keys when updating JSON state
- Accurate recall of the most recent value across sessions

## Sessions

1. **Store Initial Value** -- Write the key "color" with value "blue" to memory.json
2. **Overwrite Value** -- Update the key "color" to "red" in memory.json (must replace, not append)
3. **Recall Value** -- Read memory.json and write the current value of "color" to answer.txt

## Constraints

- `setup/memory.json` must contain exactly ONE entry for the key "color"
- `setup/answer.txt` must contain exactly the string "red"
