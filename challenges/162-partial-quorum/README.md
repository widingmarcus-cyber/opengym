# Challenge 162: Partial Quorum

## Difficulty: Hard
## Category: Agent Collaboration
## Dimension: Multi-Agent

## Description

Three nodes participate in a distributed commit protocol. Two nodes vote "commit" but the third is unavailable. A coordinator must determine whether quorum (2 out of 3) is reached and make a decision. This tests distributed consensus with partial availability.

## Objective

- **Node A** casts a "commit" vote
- **Node B** casts a "commit" vote (Node C is unavailable)
- **Coordinator** evaluates quorum and makes a commit/abort decision

## Setup

- `setup/` -- empty directory at start

## Steps

1. **Step 1 (Node A):** Read `steps/step_1.md`. Cast your vote.
2. **Step 2 (Node B):** Read `steps/step_2.md`. Cast your vote.
3. **Step 3 (Coordinator):** Read `steps/step_3.md`. Evaluate quorum and decide.

## Verification

```bash
python tests/verify.py
```

Checks that votes.json has 2 entries, and answer.json has quorum_reached=true with decision="commit".
