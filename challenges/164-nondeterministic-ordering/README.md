# Challenge 164: Non-deterministic Ordering Exposure

## Difficulty: Medium
## Category: Agent Collaboration
## Dimension: Multi-Agent

## Description

Tasks are provided in a scrambled order. An agent must process all tasks and produce results that are deterministically sorted by task ID, regardless of the order they were processed. This tests whether agents can ensure deterministic output from non-deterministic input.

## Objective

- Process tasks that arrive in scrambled order
- Produce results sorted by task ID
- Verify the output is correctly sorted

## Setup

- `setup/tasks.json` -- pre-created with 6 tasks in scrambled order

## Steps

1. **Step 1 (Processor):** Read `steps/step_1.md`. Process tasks and produce sorted results.
2. **Step 2 (Verifier):** Read `steps/step_2.md`. Verify sorting and write the answer.

## Verification

```bash
python tests/verify.py
```

Checks that results.json has 6 sorted entries and answer.txt = "SORTED".
