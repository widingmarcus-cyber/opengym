# Challenge 140: Memory Corruption Detection

## Difficulty: Medium

## Type: Multi-Session (2 steps)

## Dimension: Memory

## Overview

This challenge tests whether your agent can detect data corruption by verifying checksums and restore data from a known-good backup. The setup provides a tampered data file alongside the checksum of the original, plus a backup copy of the original data.

## How It Works

- **Step 1:** Verify data integrity by comparing `setup/data.json` against the SHA-256 hash stored in `setup/data.checksum`. If the hash does not match, the data has been corrupted. Write `CORRUPTED` or `VALID` to `setup/status.txt`.
- **Step 2:** If the data was corrupted, restore it from `setup/backup.json` (the original). Recompute the SHA-256 checksum and save it to `setup/data.checksum`. Write `RESTORED` to `setup/status.txt`.

## Rules

- Only modify files in the `setup/` directory
- The SHA-256 hash must be computed on the exact file contents (UTF-8 encoding)
- The files `setup/data.json`, `setup/data.checksum`, and `setup/backup.json` persist between sessions

## What Gets Persisted Between Sessions

Only files listed in `metadata.yaml` under `persist` survive between steps.

## Scoring

You pass if:
- `setup/status.txt` contains `RESTORED`
- `setup/data.json` matches `setup/backup.json` in content
- `setup/data.checksum` matches the actual SHA-256 hash of `setup/data.json`
