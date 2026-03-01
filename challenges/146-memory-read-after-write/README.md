# Challenge 146: Memory Read-After-Write Delay

## Difficulty: Medium

## Type: Multi-Session (3 steps)

## Dimension: Memory

## Overview

This challenge tests whether your agent can handle simulated consistency delays in file-based state management. A flag file indicates a write is in progress. The agent must recognize this signal and proceed only when the flag is gone. Between sessions, non-persisted files are cleaned up, so the flag naturally disappears.

## How It Works

- **Step 1:** Write an initial version of the store to `setup/store.json`.
- **Step 2:** A `setup/pending_write.flag` file existed (simulating an in-progress write), but since it is not in the persist list, it has been cleaned up between sessions. Confirm the flag is gone, then update the store.
- **Step 3:** Read the store and write the version number to `setup/answer.txt`.

## Rules

- Only modify files in the `setup/` directory
- The `pending_write.flag` file is NOT persisted between sessions -- it gets cleaned up automatically
- Only `setup/store.json` persists between sessions
- Do not update the store while a write flag is present

## What Gets Persisted Between Sessions

Only files listed in `metadata.yaml` under `persist` survive between steps.

## Scoring

You pass if:
- `setup/answer.txt` contains `2`
- `setup/store.json` has `version: 2` and `data: "updated"`
