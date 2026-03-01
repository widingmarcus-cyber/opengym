# Challenge 145: Memory Integrity Checksum

## Difficulty: Medium

## Type: Multi-Session (2 steps)

## Dimension: Memory

## Overview

This challenge tests whether your agent can implement data integrity verification using checksums. You will write data to a file, compute its SHA-256 checksum, and then in a later session verify that the data has not been tampered with by comparing checksums.

## How It Works

- **Step 1:** Write a specific JSON object to `setup/data.json`. Compute the SHA-256 hash of the file contents and save it to `setup/checksum.txt`.
- **Step 2:** Read `setup/data.json` and `setup/checksum.txt`. Recompute the SHA-256 hash of `data.json` and compare it to the stored checksum. Write `VALID` or `INVALID` to `setup/status.txt`.

## Rules

- Only modify files in the `setup/` directory
- The SHA-256 hash must be computed on the exact byte contents of `data.json`
- The checksum in `checksum.txt` should be the hex-encoded SHA-256 digest
- The files `setup/data.json` and `setup/checksum.txt` persist between sessions

## What Gets Persisted Between Sessions

Only files listed in `metadata.yaml` under `persist` survive between steps.

## Scoring

You pass if:
- `setup/status.txt` contains `VALID`
- `setup/checksum.txt` contains the correct SHA-256 hash of `setup/data.json`
