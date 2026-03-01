# Challenge 156: Delegation Retry with Backoff

## Difficulty: Hard
## Category: Task Splitting
## Dimension: Multi-Agent

## Description

An agent must execute a task that fails on the first two attempts, implementing an exponential backoff retry strategy. The agent must track each attempt, log the retry pattern, and eventually succeed on the third attempt.

This challenge tests whether agents can implement robust retry logic with proper backoff patterns -- a critical pattern in distributed systems and fault-tolerant coordination.

## Objective

- Read the attempt counter, increment it, and determine if the task "succeeds" (counter >= 3) or "fails" (counter < 3)
- Log each attempt with its status and wait time (exponential backoff)
- After success, analyze the retry log and summarize the pattern

## Setup

- `setup/attempt_counter.txt` -- starts at "0"

## Steps

1. **Step 1 (Executor):** Read `steps/step_1.md`. Execute the task with retry logic and exponential backoff.
2. **Step 2 (Analyzer):** Read `steps/step_2.md`. Analyze the retry log and write the summary.

## Verification

```bash
python tests/verify.py
```

Checks that result.txt = "SUCCESS", retry_log.json has 3 entries with exponential backoff, and answer.json is correct.
