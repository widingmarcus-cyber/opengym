"""Writer script — reads data.csv and writes result.csv.
Only works if workspace is under quota. DO NOT MODIFY this file."""

import csv
import json
import os

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.join(SETUP_DIR, "workspace")

def get_workspace_size():
    total = 0
    for fname in os.listdir(WORKSPACE):
        total += os.path.getsize(os.path.join(WORKSPACE, fname))
    return total

def run():
    with open(os.path.join(SETUP_DIR, "quota.json")) as f:
        quota = json.load(f)

    current_size = get_workspace_size()
    max_bytes = quota["max_bytes"]

    if current_size > max_bytes:
        raise RuntimeError(
            f"Disk full: workspace is {current_size} bytes but quota is {max_bytes} bytes. "
            f"Clean up {current_size - max_bytes} bytes first."
        )

    # Read data.csv and produce result.csv
    input_path = os.path.join(WORKSPACE, "data.csv")
    output_path = os.path.join(WORKSPACE, "result.csv")

    with open(input_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "score", "grade"])
        writer.writeheader()
        for row in rows:
            score = int(row["score"])
            if score >= 90:
                grade = "A"
            elif score >= 80:
                grade = "B"
            elif score >= 70:
                grade = "C"
            else:
                grade = "D"
            writer.writerow({**row, "grade": grade})

    print(f"Wrote {len(rows)} records to result.csv")

if __name__ == "__main__":
    run()
