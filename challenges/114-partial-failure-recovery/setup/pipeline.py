import json
from pathlib import Path

RATES = {"USD": 1.0, "EUR": 1.1, "GBP": 1.27, "JPY": 0.0067}
MULTIPLIERS = {"standard": 1.0, "premium": 1.5}  # BUG 1: missing "express" type

def process_record(record):
    """Process a single record."""
    value = float(record["value"])  # BUG 3: crashes on values like "425.00 USD"

    if value < 0:  # BUG 2: negative values should be converted to absolute value, not rejected
        raise ValueError(f"Negative value not allowed: {value}")

    rate = RATES[record["currency"]]
    multiplier = MULTIPLIERS[record["type"]]  # BUG 1: KeyError for "express"

    return {
        "id": record["id"],
        "usd_value": round(value * rate * multiplier, 2),
        "original_currency": record["currency"],
    }

def process_all(input_file, output_file):
    """Process all records from input file."""
    data_dir = Path(__file__).parent
    with open(data_dir / input_file) as f:
        records = json.load(f)

    results = []
    for record in records:
        result = process_record(record)
        results.append(result)

    with open(data_dir / output_file, "w") as f:
        json.dump(results, f, indent=2)

    return results
