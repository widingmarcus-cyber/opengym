# Challenge 161: Barrier Synchronization

## Difficulty: Hard
## Category: Agent Collaboration
## Dimension: Multi-Agent

## Description

Two worker agents must complete their independent tasks and signal readiness at a barrier before an aggregator can combine their results. This tests barrier synchronization -- a fundamental coordination primitive in parallel computing.

## Objective

- **Worker A** completes a computation and signals readiness
- **Worker B** completes a computation and signals readiness
- **Aggregator** waits for both workers to be ready, then combines results

## Setup

- `setup/barrier.json` -- will track worker readiness
- `setup/results/` -- directory for individual worker results

## Steps

1. **Step 1 (Worker A):** Read `steps/step_1.md`. Complete task and mark ready at barrier.
2. **Step 2 (Worker B):** Read `steps/step_2.md`. Complete task and mark ready at barrier.
3. **Step 3 (Aggregator):** Read `steps/step_3.md`. Check barrier and combine results.

## Verification

```bash
python tests/verify.py
```

Checks that both workers signaled readiness, both result files exist, and the aggregated answer has the correct total.
