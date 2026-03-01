# Challenge 195: Clock Skew

**Difficulty:** medium
**Category:** task-sequencing
**Dimension:** planning
**Type:** single-session

## Description

In distributed systems, clock skew between nodes can cause coordination problems. Given timestamps reported by different nodes, calculate the maximum clock skew and determine if it falls within an acceptable tolerance.

## Objectives

- Read `setup/node_times.json` which contains timestamps from three nodes.
- Calculate the skew (time difference) between each pair of nodes.
- Find the maximum skew.
- Determine if the maximum skew is within the acceptable tolerance of 3 seconds.
- Write `setup/answer.json` with the results.

## Data

Node times (all supposedly the "same" moment):
- node_a: 2024-01-01T12:00:00Z
- node_b: 2024-01-01T12:00:05Z (5 seconds ahead of node_a)
- node_c: 2024-01-01T11:59:55Z (5 seconds behind node_a)

Max acceptable skew: 3 seconds

Pairwise skews:
- node_a vs node_b: 5 seconds
- node_a vs node_c: 5 seconds
- node_b vs node_c: 10 seconds (worst pair)

## Expected Output

`setup/answer.json`:
```json
{
  "max_skew_seconds": 10,
  "within_tolerance": false,
  "worst_pair": ["node_b", "node_c"]
}
```
