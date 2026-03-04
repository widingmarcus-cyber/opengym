# Challenge 242: Five-Session Cumulative State Machine

## Difficulty: Hard
## Type: Multi-Session (5 steps)
## Dimension: Memory

## Overview

Build and maintain a key-value store across 5 independent sessions. Each session adds data, modifies constraints, and queries the store. You must persist everything to `setup/store.json` between sessions.

## How It Works

- **Step 1:** Create the initial store with 10 entries.
- **Step 2:** Add 8 new entries and upgrade all existing entries to version 2.
- **Step 3:** Compact the store by removing expired temp entries. Write a compaction report.
- **Step 4:** Answer analytical queries about the store.
- **Step 5:** Compute a SHA256 integrity checksum and write a manifest.

## Entry Format

Each entry in the store is a JSON object with these fields:

```json
{
  "key": "example_key",
  "value": "any JSON value",
  "tag": "config",
  "version": 1,
  "timestamp": "2025-11-01T09:00:00Z"
}
```

The store itself is a JSON object mapping keys to entry objects:

```json
{
  "example_key": { "key": "example_key", "value": "...", "tag": "...", "version": 1, "timestamp": "..." }
}
```

## Rules

- Only modify files in the `setup/` directory.
- The file `setup/store.json` persists between all sessions.
- All other `setup/*.json` files also persist between sessions.
- Use the exact keys, values, and tags specified in each step.
- Timestamps must be valid ISO 8601 strings.

## What Gets Persisted Between Sessions

Only files matching `setup/*.json` survive between steps. Everything else may be deleted by the runner.

## Scoring

You pass if all output files contain correct values after all 5 steps have been completed.
