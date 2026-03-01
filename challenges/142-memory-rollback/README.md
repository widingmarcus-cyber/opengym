# Challenge 142: Memory Rollback

## Difficulty: Hard

## Type: Multi-Session (3 steps)

## Dimension: Memory

## Overview

This challenge tests whether your agent can implement transactional state management with rollback capability. You will manage a balance with transactions, maintain a version history, and roll back to a previous state when a transaction fails validation.

## How It Works

- **Step 1:** Initialize state with a balance of 100 and empty transactions list. Create a version history log.
- **Step 2:** Process two transactions: a valid withdrawal of 30 (succeeds) and an invalid withdrawal of 200 (fails due to insufficient funds). Roll back to the state after the successful transaction.
- **Step 3:** Read the final state and write the balance to `setup/answer.txt`.

## Rules

- Only modify files in the `setup/` directory
- A withdrawal fails if the amount exceeds the current balance
- On failure, the state must be rolled back to the last successful version
- The files `setup/state.json` and `setup/history.json` persist between sessions

## What Gets Persisted Between Sessions

Only files listed in `metadata.yaml` under `persist` survive between steps.

## Scoring

You pass if:
- `setup/answer.txt` contains `70`
- `setup/state.json` has `balance: 70` and exactly 1 transaction (the successful withdrawal of 30)
- `setup/history.json` has versions 1 and 2
