# Challenge 225: Trace Reconstruction

## Objective

Reconstruct a distributed trace tree from flat span data.

## Context

In distributed tracing (e.g., OpenTelemetry, Jaeger), each operation creates a "span" with a trace ID, span ID, and optional parent span ID. Spans arrive out of order from different services. Reconstructing the full trace tree — with correct parent-child relationships and computed durations — is essential for understanding request flow and diagnosing latency.

## Task

Read `setup/spans.json` which contains a flat array of span objects:

```json
{
  "trace_id": "abc123",
  "span_id": "span-1",
  "parent_span_id": null,
  "service": "api-gateway",
  "operation": "GET /users",
  "start_time_ms": 1000,
  "end_time_ms": 1250
}
```

Build the trace tree and write `setup/trace.json` with the following structure:

```json
{
  "trace_id": "abc123",
  "root": {
    "span_id": "span-1",
    "service": "api-gateway",
    "operation": "GET /users",
    "start_time_ms": 1000,
    "end_time_ms": 1250,
    "duration_ms": 250,
    "children": [
      {
        "span_id": "span-2",
        "service": "user-service",
        "operation": "fetchUser",
        "start_time_ms": 1010,
        "end_time_ms": 1200,
        "duration_ms": 190,
        "children": []
      }
    ]
  },
  "total_spans": 2,
  "total_duration_ms": 250,
  "critical_path_ms": 250
}
```

## Requirements

- Identify the root span (the one with `parent_span_id` of `null`)
- Build the tree by matching `parent_span_id` to `span_id`
- Calculate `duration_ms` for each span (`end_time_ms - start_time_ms`)
- Children should be ordered by `start_time_ms` (ascending)
- `total_spans`: count of all spans in the trace
- `total_duration_ms`: duration of the root span
- `critical_path_ms`: the longest path from root to any leaf (sum of durations along the deepest branch where each child's duration contributes to latency)

## Verification

```bash
python3 tests/verify.py
```
