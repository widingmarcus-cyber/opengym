# Challenge 139: Memory Conflict Resolution

## Difficulty: Hard

## Type: Multi-Session (3 steps)

## Dimension: Memory

## Overview

This challenge tests whether your agent can handle concurrent-style write conflicts to shared state using a conflict resolution policy. Two simulated agents write to the same config file, and the correct final state depends on the declared policy.

## How It Works

- **Step 1:** Initialize shared state in `setup/state.json` with a config object, and write the conflict resolution policy to `setup/policy.txt`.
- **Step 2 (Agent A):** Update a config value in `setup/state.json`.
- **Step 3 (Agent B):** Read the conflict resolution policy from `setup/policy.txt`, apply it, write the final value to `setup/state.json`, and record the result in `setup/answer.txt`.

## Rules

- Only modify files in the `setup/` directory
- The conflict resolution policy in `setup/policy.txt` must be respected
- Files `setup/state.json` and `setup/policy.txt` persist between sessions

## What Gets Persisted Between Sessions

Only files listed in `metadata.yaml` under `persist` survive between steps.

## Scoring

You pass if:
- `setup/state.json` has `port: 9090`
- `setup/answer.txt` contains `9090`
- `setup/policy.txt` contains `last-write-wins`
