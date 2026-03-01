# Challenge 103: Incremental Knowledge

## Difficulty: Medium

## Type: Multi-Session (4 steps)

## Dimension: Memory

## Overview

This challenge tests whether you can accumulate requirements across multiple sessions and produce a final configuration that satisfies all of them. Each session reveals one new constraint for a server configuration. You must track all constraints in a persistent file and, in the final session, produce a complete configuration.

## How It Works

- **Step 1:** First requirement arrives (port and TLS). Create `setup/constraints.json` to track it.
- **Step 2:** Second requirement arrives (rate limiting). Add it to your existing constraints.
- **Step 3:** Third requirement arrives (logging). Add it to your constraints.
- **Step 4:** Read all accumulated constraints from `setup/constraints.json` and write the complete server configuration to `setup/server_config.json`.

## Rules

- Only modify files in the `setup/` directory
- Each step adds exactly one new requirement — do not skip ahead
- Your `setup/constraints.json` must persist between all sessions
- The final config must satisfy ALL requirements from all 4 steps

## What Gets Persisted Between Sessions

- `setup/constraints.json` — your accumulated requirements
- `setup/server_config.json` — the final output (only needed in step 4)

## Scoring

The final `setup/server_config.json` is validated against all requirements:
- Correct port (8443) and TLS settings (enabled, version 1.3)
- Correct rate limiting (100 req/min, burst 20)
- Correct logging (stdout at INFO, file at /var/log/app.log at DEBUG)
