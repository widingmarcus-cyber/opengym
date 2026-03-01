# Challenge 122: Information Asymmetry

## Difficulty: Hard
## Category: Agent Collaboration
## Dimension: Multi-Agent

## Description

Three agents must collaborate to diagnose and fix a bug, but each agent has access to different information. They must communicate through a shared messages file to pass knowledge between stages.

- **Agent 1 (Diagnostics):** Has access to the error log but not the source code.
- **Agent 2 (Code Review):** Has access to the source code and the diagnosis from Agent 1.
- **Agent 3 (Implementation):** Reads all messages and applies the fix.

This tests whether agents can extract relevant information, communicate it clearly, and act on information provided by other agents.

## Objective

Fix `UserService.get_profile()` so that it handles legacy user IDs (format `L-{id}`) when an integer lookup returns None.

## Setup

- `setup/error_log.txt` — error log showing the failure
- `setup/services/user.py` — the broken service code
- `setup/repos/user.py` — the repository with the user database
- `setup/messages.json` — shared communication channel (created by agents)

## Steps

1. **Step 1 (Diagnostics Agent):** Analyze the error log and write diagnosis to messages.json.
2. **Step 2 (Code Agent):** Read diagnosis, examine code, write fix instructions to messages.json.
3. **Step 3 (Implementation Agent):** Read all messages and apply the fix to services/user.py.

## Verification

```bash
python tests/verify.py
```

Tests that the fixed code correctly handles both legacy and modern user ID lookups.
