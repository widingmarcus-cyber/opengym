"""Record processor with idempotency bugs.

This script processes input records and writes results.
BUG: Running this script multiple times produces different/corrupted output.
Your task is to make it idempotent — running it N times should produce
the same result as running it once.
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "input_records.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "output.json")
STATE_PATH = os.path.join(SCRIPT_DIR, "state.json")


def load_state():
    """Load persistent state, or create default."""
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            return json.load(f)
    return {"processed_count": 0, "total_amount": 0.0}


def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def process():
    # Load input
    with open(INPUT_PATH) as f:
        records = json.load(f)

    # Load existing state
    state = load_state()

    # Process each record (BUG: no deduplication by id)
    processed = []
    for record in records:
        processed.append({
            "id": record["id"],
            "name": record["name"],
            "email": record["email"],
            "amount": record["amount"],
            "status": "processed"
        })

    # BUG: Appends to existing output instead of overwriting
    existing = []
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH) as f:
            existing = json.load(f)

    all_records = existing + processed

    with open(OUTPUT_PATH, "w") as f:
        json.dump(all_records, f, indent=2)

    # BUG: Accumulates counter across runs instead of setting it
    state["processed_count"] += len(processed)
    state["total_amount"] += sum(r["amount"] for r in processed)
    save_state(state)

    print(f"Processed {len(processed)} records. Total in output: {len(all_records)}")


if __name__ == "__main__":
    process()
