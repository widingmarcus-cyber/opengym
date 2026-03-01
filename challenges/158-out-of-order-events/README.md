# Challenge 158: Out-of-Order Event Handling

## Difficulty: Medium
## Category: Agent Collaboration
## Dimension: Multi-Agent

## Description

Events arrive out of sequence order. An agent must sort them by their sequence number and then extract the data in the correct order. This tests whether agents can handle non-sequential event delivery -- a common challenge in distributed message systems.

## Objective

- Sort out-of-order events by their sequence number
- Extract the data values in the correct order
- Produce a comma-separated string of the ordered data

## Setup

- `setup/events.json` -- pre-created with 5 events in scrambled order

## Steps

1. **Step 1 (Sorter):** Read `steps/step_1.md`. Sort events by sequence number.
2. **Step 2 (Extractor):** Read `steps/step_2.md`. Extract ordered data values.

## Verification

```bash
python tests/verify.py
```

Checks that ordered.json has events sorted by seq 1-5, and answer.txt contains the correct comma-separated string.
