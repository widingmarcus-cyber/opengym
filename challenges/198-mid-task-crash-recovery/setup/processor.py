"""Data processor — this script crashed mid-task. Fix the bug and use it to resume processing."""

import json

PRICE_LOOKUP = {
    "apple": 2, "banana": 3, "cherry": 1, "date": 4, "elderberry": 0,
    "fig": 5, "grape": 2, "honeydew": 6, "kiwi": 3, "lemon": 1
}

def transform_record(record):
    """Transform a single record. BUG: crashes when price is 0."""
    unit_price = record['quantity'] / PRICE_LOOKUP[record['value']]
    result_str = f"{record['value'].upper()}_x{record['quantity']}"
    return {
        **record,
        "status": "processed",
        "result": result_str
    }

def process_all(input_path, output_path):
    with open(input_path) as f:
        records = json.load(f)
    results = []
    for rec in records:
        results.append(transform_record(rec))
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    process_all("input_records.json", "output.json")
