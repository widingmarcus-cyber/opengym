# Challenge 143: Memory Snapshot Restore

## Difficulty: Hard

## Type: Multi-Session (3 steps)

## Dimension: Memory

## Overview

This challenge tests whether your agent can manage state with snapshots and restore from a previous snapshot when something goes wrong. You will initialize state, take snapshots at key points, modify state, and then restore from an earlier snapshot.

## How It Works

- **Step 1:** Initialize `setup/state.json` with an initial state. Save a snapshot copy to `setup/snapshots/snap_1.json`.
- **Step 2:** Modify the state (add a user, change config). Save another snapshot. Then restore state from snap_1.json because something went wrong.
- **Step 3:** Read the restored state and write the theme value to `setup/answer.txt`.

## Rules

- Only modify files in the `setup/` directory
- Snapshots are exact copies of `state.json` at the time they are taken
- When restoring, overwrite `state.json` with the contents of the target snapshot
- The files `setup/state.json` and `setup/snapshots/` persist between sessions

## What Gets Persisted Between Sessions

Only files listed in `metadata.yaml` under `persist` survive between steps.

## Scoring

You pass if:
- `setup/answer.txt` contains `light`
- `setup/state.json` has `users: ["alice"]` and `config.theme: "light"`
- `setup/snapshots/snap_1.json` and `setup/snapshots/snap_2.json` both exist
