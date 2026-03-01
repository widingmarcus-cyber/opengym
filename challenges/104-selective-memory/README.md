# Challenge 104: Selective Memory

**Difficulty:** Hard
**Category:** memory-filtering
**Dimension:** memory
**Type:** Multi-session (3 steps)

## Objective

You receive 50 project records, but only 5 are marked as IMPORTANT. Store only the important ones in memory (under 2KB), survive a distraction task, then recall them accurately from memory alone.

## What This Tests

- Ability to filter and prioritize information
- Memory efficiency under storage constraints
- Recall accuracy after context disruption
- Selective attention in noisy data

## Sessions

1. **Read & Filter** — Read 50 records, store only the IMPORTANT ones in memory.json (max 2KB)
2. **Distraction** — Implement a binary search function (unrelated task)
3. **Recall** — The original records are gone. Using only memory.json, list all important projects with correct details.

## Constraints

- `setup/memory.json` must be under 2KB
- Only IMPORTANT records should be stored
- Final answers must include project name, budget (as number), and status
