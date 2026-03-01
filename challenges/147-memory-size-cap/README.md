# Challenge 147: Memory Size Cap Enforcement

## Difficulty: Hard

## Type: Multi-Session (2 steps)

## Dimension: Memory

## Overview

This challenge tests whether your agent can make intelligent decisions about what data to store when facing a hard storage constraint. You are given 50 records to store, but the storage file must not exceed 1024 bytes. Only 10 of the 50 records are marked as IMPORTANT -- you must prioritize those.

## How It Works

- **Step 1:** You receive 50 records. Store as many as you can in `setup/memory.json`, but the file must not exceed 1024 bytes. Records marked `IMPORTANT` must be prioritized.
- **Step 2:** Read `setup/memory.json` and write the count of stored records to `setup/answer.txt`.

## Rules

- Only modify files in the `setup/` directory
- `setup/memory.json` must be valid JSON
- `setup/memory.json` file size must not exceed 1024 bytes
- All 10 IMPORTANT records must be present in the stored data
- The file `setup/memory.json` persists between sessions

## What Gets Persisted Between Sessions

Only files listed in `metadata.yaml` under `persist` survive between steps.

## Scoring

You pass if:
- `setup/memory.json` file size is at most 1024 bytes
- All 10 IMPORTANT records are present in the file
- `setup/answer.txt` contains the count of stored records
