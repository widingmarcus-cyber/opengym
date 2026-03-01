# Challenge 163: Multi-Agent File Append Ordering

## Difficulty: Medium
## Category: Shared Resources
## Dimension: Multi-Agent

## Description

Three agents must sequentially append lines to a shared log file. Each agent must preserve all previous content and append exactly one line. This tests whether agents can safely perform ordered append operations on a shared resource.

## Objective

- **Agent A** appends the first line to the log
- **Agent B** appends the second line, preserving Agent A's line
- **Agent C** appends the third line, preserving both previous lines, and counts the total

## Setup

- `setup/log.txt` -- empty file at start

## Steps

1. **Step 1 (Agent A):** Read `steps/step_1.md`. Append your line to the log.
2. **Step 2 (Agent B):** Read `steps/step_2.md`. Append your line, preserving existing content.
3. **Step 3 (Agent C):** Read `steps/step_3.md`. Append your line and count total lines.

## Verification

```bash
python tests/verify.py
```

Checks that log.txt has 3 lines in order (A:step1, B:step2, C:step3) and answer.txt = "3".
