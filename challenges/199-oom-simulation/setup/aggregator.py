"""Aggregator — this script OOMs because it loads everything into memory at once.
Rewrite it to use chunked/streaming processing."""

import json
import glob
import os

def aggregate_all():
    """BUG: Loads all data into one giant list — causes OOM on large datasets."""
    all_records = []
    chunk_files = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "data_chunks", "*.json")))

    # BAD: accumulates everything in memory
    for fpath in chunk_files:
        with open(fpath) as f:
            data = json.load(f)
            all_records.extend(data)

    # BAD: sorts the entire list in memory
    all_records.sort(key=lambda r: r["value"])

    summary = {
        "total_records": len(all_records),
        "sum_value": sum(r["value"] for r in all_records),
        "avg_value": round(sum(r["value"] for r in all_records) / len(all_records), 2),
        "max_value": max(r["value"] for r in all_records),
        "min_value": min(r["value"] for r in all_records),
        "processing_method": "bulk"
    }

    with open(os.path.join(os.path.dirname(__file__), "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    aggregate_all()
