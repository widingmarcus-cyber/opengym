# Challenge 224: Metric Aggregation

## Objective

Aggregate raw metric datapoints into statistical summaries per metric name.

## Context

Observability systems collect millions of raw metric datapoints per minute. To be useful for dashboards and alerting, these must be aggregated into statistical summaries — min, max, average, and percentiles — over defined time windows.

## Task

Read `setup/metrics.csv` which contains timestamped metric values with columns:

```
timestamp,metric_name,value
```

Compute aggregations **per metric name** and write `setup/summary.json` with the following structure:

```json
{
  "metric_name": {
    "count": 100,
    "min": 1.0,
    "max": 99.5,
    "avg": 45.2,
    "p50": 44.0,
    "p95": 92.1,
    "p99": 98.3
  }
}
```

## Requirements

- Read all rows from `metrics.csv`
- Group by `metric_name`
- For each metric, compute: `count`, `min`, `max`, `avg` (arithmetic mean), `p50` (median), `p95`, `p99`
- Round all floating point values to 2 decimal places
- Use nearest-rank method for percentile calculation
- Write output as `setup/summary.json`

## Verification

```bash
python3 tests/verify.py
```
