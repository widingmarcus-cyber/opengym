# Challenge 121: Shared Config

## Difficulty: Medium
## Category: Shared Resources
## Dimension: Multi-Agent

## Description

Two agents must collaborate to build a shared application configuration file. Each agent is responsible for writing a different section of the config without overwriting the other agent's work.

This challenge tests whether agents can safely perform concurrent writes to a shared resource — a common real-world coordination problem.

## Objective

- **Agent A** writes the `database` section to `setup/shared_config.yaml`
- **Agent B** writes the `cache` section to `setup/shared_config.yaml`
- Both sections must coexist in the final file — neither agent should overwrite the other's work.

## Setup

- `setup/shared_config.yaml` — a starter config file with only comments

## Steps

1. **Step 1 (Agent A):** Read `steps/step_1.md` and follow instructions to write the database section.
2. **Step 2 (Agent B):** Read `steps/step_2.md` and follow instructions to write the cache section.

## Verification

```bash
python tests/verify.py
```

Checks that both `database` and `cache` sections exist with correct values, and neither overwrote the other.
