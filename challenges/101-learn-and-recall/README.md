# Challenge 101: Learn and Recall

## Difficulty: Easy

## Type: Multi-Session (3 steps)

## Dimension: Memory

## Overview

This challenge tests whether your memory system can persist facts across sessions. You will read user preferences, do unrelated work (to flood your context), and then recall the preferences after the source file has been deleted.

## How It Works

- **Step 1:** Read a user profile and store the preferences externally in `setup/memory.json`.
- **Step 2:** Solve an unrelated coding task (distractor). This floods your context with irrelevant work.
- **Step 3:** The original profile file has been deleted. Using only your stored data in `setup/memory.json`, answer questions about the user's preferences.

## Rules

- Only modify files in the `setup/` directory
- In step 3, you must NOT read `setup/user_profile.txt` (it will have been deleted)
- Your answers in step 3 must come from your persisted memory (`setup/memory.json`)
- The file `setup/memory.json` is the only file that persists between all sessions

## What Gets Persisted Between Sessions

Only files listed in `metadata.yaml` under `persist` survive between steps. Everything else in `setup/` may be deleted by the runner between steps.

## Scoring

You pass if `setup/answers.json` contains the correct values for all 5 queried fields.
