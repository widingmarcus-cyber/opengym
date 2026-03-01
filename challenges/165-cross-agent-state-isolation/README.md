# Challenge 165: Cross-Agent State Isolation

## Difficulty: Medium
## Category: Shared Resources
## Dimension: Multi-Agent

## Description

Two agents each have private state containing secrets. They must share only their data (not secrets) via a shared output file. A third step verifies that secrets were not leaked into the shared output. This tests information isolation in multi-agent systems.

## Objective

- **Agent A** writes private state (with a secret) and shares only data to shared output
- **Agent B** writes private state (with a secret) and shares only data to shared output, without reading Agent A's private state
- **Step 3** verifies no secrets leaked and counts total shared items

## Setup

- `setup/` -- empty directory at start

## Steps

1. **Step 1 (Agent A):** Read `steps/step_1.md`. Write private state and share data.
2. **Step 2 (Agent B):** Read `steps/step_2.md`. Write private state and share data.
3. **Step 3 (Auditor):** Read `steps/step_3.md`. Verify isolation and produce summary.

## Verification

```bash
python tests/verify.py
```

Checks that shared_output.json has both data arrays but no secrets, private state files have secrets, and answer.json is correct.
